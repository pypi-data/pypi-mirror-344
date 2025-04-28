# Copyright 2024 The Langfun Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for base action."""

import unittest

import langfun.core as lf
from langfun.core.agentic import action as action_lib
from langfun.core.llms import fake
import langfun.core.structured as lf_structured
import pyglove as pg


class SessionTest(unittest.TestCase):

  def test_basics(self):
    test = self

    class Bar(action_lib.Action):

      def call(self, session, *, lm, **kwargs):
        test.assertIs(session.current_action.action, self)
        session.info('Begin Bar')
        session.query('bar', lm=lm)
        session.add_metadata(note='bar')
        return 2

    class Foo(action_lib.Action):
      x: int

      def call(self, session, *, lm, **kwargs):
        test.assertIs(session.current_action.action, self)
        with session.track_phase('prepare'):
          session.info('Begin Foo', x=1)
          session.query('foo', lm=lm)
        with session.track_queries():
          self.make_additional_query(lm)
        session.add_metadata(note='foo')

        def _sub_task(i):
          session.add_metadata(**{f'subtask_{i}': i})
          return lf_structured.query(f'subtask_{i}', lm=lm)

        for i, output, error in session.concurrent_map(
            _sub_task, range(3), max_workers=2, silence_on_errors=None,
        ):
          assert isinstance(i, int), i
          assert isinstance(output, str), output
          assert error is None, error
        return self.x + Bar()(session, lm=lm)

      def make_additional_query(self, lm):
        lf_structured.query('additional query', lm=lm)

    lm = fake.StaticResponse('lm response')
    foo = Foo(1)
    self.assertEqual(foo(lm=lm, verbose=True), 3)

    session = foo.session
    self.assertIn('session@', session.id)
    self.assertIsNotNone(session)
    self.assertIsInstance(session.root.action, action_lib.RootAction)
    self.assertIs(session.current_action, session.root)

    #
    # Inspecting the root invocation.
    #

    root = session.root
    self.assertEqual(len(root.execution.items), 1)
    self.assertIs(root.execution.items[0].action, foo)

    self.assertTrue(root.execution.has_started)
    self.assertTrue(root.execution.has_stopped)
    self.assertGreater(root.execution.elapse, 0)
    self.assertEqual(root.result, 3)
    self.assertEqual(
        root.metadata,
        dict(note='foo', subtask_0=0, subtask_1=1, subtask_2=2)
    )

    # The root space should have one action (foo), no queries, and no logs.
    self.assertEqual(len(list(root.actions)), 1)
    self.assertEqual(len(list(root.queries)), 0)
    self.assertEqual(len(list(root.logs)), 0)
    # 1 query from Bar, 2 from Foo and 3 from parallel executions.
    self.assertEqual(len(list(root.all_queries)), 6)
    # 2 actions: Foo and Bar.
    self.assertEqual(len(list(root.all_actions)), 2)
    # 1 log from Bar and 1 from Foo.
    self.assertEqual(len(list(root.all_logs)), 2)
    self.assertEqual(root.usage_summary.total.num_requests, 6)

    # Inspecting the top-level action (Foo)
    foo_invocation = root.execution.items[0]
    self.assertEqual(len(foo_invocation.execution.items), 4)

    # Prepare phase.
    prepare_phase = foo_invocation.execution.items[0]
    self.assertIsInstance(
        prepare_phase, action_lib.ExecutionTrace
    )
    self.assertEqual(len(prepare_phase.items), 2)
    self.assertTrue(prepare_phase.has_started)
    self.assertTrue(prepare_phase.has_stopped)
    self.assertEqual(prepare_phase.usage_summary.total.num_requests, 1)

    # Tracked queries.
    query_invocation = foo_invocation.execution.items[1]
    self.assertIsInstance(query_invocation, lf_structured.QueryInvocation)
    self.assertIs(query_invocation.lm, lm)

    # Tracked parallel executions.
    parallel_executions = foo_invocation.execution.items[2]
    self.assertIsInstance(parallel_executions, action_lib.ParallelExecutions)
    self.assertEqual(len(parallel_executions), 3)
    self.assertEqual(len(parallel_executions[0].queries), 1)
    self.assertEqual(len(parallel_executions[1].queries), 1)
    self.assertEqual(len(parallel_executions[2].queries), 1)

    # Invocation to Bar.
    bar_invocation = foo_invocation.execution.items[3]
    self.assertIsInstance(bar_invocation, action_lib.ActionInvocation)
    self.assertIsInstance(bar_invocation.action, Bar)
    self.assertEqual(bar_invocation.result, 2)
    self.assertEqual(bar_invocation.metadata, dict(note='bar'))
    self.assertEqual(len(bar_invocation.execution.items), 2)

    # Save to HTML
    self.assertIn('result', session.to_html().content)

    # Save session to JSON
    json_str = session.to_json_str(save_ref_value=True)
    self.assertIsInstance(pg.from_json_str(json_str), action_lib.Session)

  def test_log(self):
    session = action_lib.Session()
    session.debug('hi', x=1, y=2)
    session.info('hi', x=1, y=2)
    session.warning('hi', x=1, y=2)
    session.error('hi', x=1, y=2)
    session.fatal('hi', x=1, y=2)

  def test_as_message(self):
    session = action_lib.Session(id='abc')
    self.assertEqual(session.id, 'abc')
    self.assertIsInstance(session.as_message(), lf.AIMessage)


if __name__ == '__main__':
  unittest.main()
