"""
Tests for the models that configures the
LTI disabled fields feature.
"""
import ddt

from contextlib import contextmanager
from django.test import TestCase

from opaque_keys.edx.locator import CourseLocator
from xblock_config.models import LTIConsumerHideFieldsFlag, CourseLTIConsumerHideFieldsFlag


@contextmanager
def lti_consumer_hide_fields_flags(global_flag, course_id=None, enabled_for_course=False):
    """
    Yields LTIConsumerHideFieldsFlag and CourseLTIConsumerHideFieldsFlag model
    records for unit tests

    Arguments:
        global_flag (bool): enables this feature for specific courses.

    Keyword Arguments:
        course_id (CourseLocator): course locator to control this feature for.
        enabled_for_course (bool): whether feature is enabled for 'course_id'
    """
    LTIConsumerHideFieldsFlag.objects.create(enabled=global_flag)
    if course_id:
        CourseLTIConsumerHideFieldsFlag.objects.create(course_id=course_id, enabled=enabled_for_course)
    yield


@ddt.ddt
class TestLTIConsumerHideFieldsFlag(TestCase):
    """
    Tests the behavior of the flags for lti consumer hide fields feature.
    These are set via Django admin settings.
    """
    def setUp(self):
        super(TestLTIConsumerHideFieldsFlag, self).setUp()
        self.course_id = CourseLocator(org="edx", course="course", run="run")

    @ddt.data(
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    )
    @ddt.unpack
    def test_lti_hide_fields_feature_flags(self, global_flag, enabled_for_course_1):
        """
        Test that feature flag works correctly with number of combinations of global
        and course-specific configurations.
        """
        with lti_consumer_hide_fields_flags(
            global_flag=global_flag,
            course_id=self.course_id,
            enabled_for_course=enabled_for_course_1
        ):
            self.assertEqual(
                LTIConsumerHideFieldsFlag.lti_access_to_learners_not_editable(self.course_id),
                global_flag and enabled_for_course_1
            )

    @ddt.data(True, False)
    def test_lti_hide_fields_flag_no_course_id(self, global_flag):
        """
        Test that enabling/disabling the feature has no effect when the course id is
        not present in course-specific configuration.
        """
        with lti_consumer_hide_fields_flags(global_flag=global_flag):
            self.assertEqual(
                LTIConsumerHideFieldsFlag.lti_access_to_learners_not_editable(self.course_id),
                False
            )

    def test_enable_disable_course_flag(self):
        """
        Ensures that the flag, once enabled for a course, can also be disabled.
        """
        with lti_consumer_hide_fields_flags(
            global_flag=True,
            course_id=self.course_id,
            enabled_for_course=True
        ):
            self.assertTrue(LTIConsumerHideFieldsFlag.lti_access_to_learners_not_editable(self.course_id))
            with lti_consumer_hide_fields_flags(
                global_flag=True,
                course_id=self.course_id,
                enabled_for_course=False
            ):
                self.assertFalse(LTIConsumerHideFieldsFlag.lti_access_to_learners_not_editable(self.course_id))
