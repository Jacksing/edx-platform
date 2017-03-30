"""
Models used by Studio XBlock infrastructure.

Includes:
    StudioConfig: A ConfigurationModel for managing Studio.
"""

from django.db.models import BooleanField, TextField
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField

from config_models.models import ConfigurationModel


class StudioConfig(ConfigurationModel):
    """
    Configuration for XBlockAsides.
    """
    disabled_blocks = TextField(
        default="about course_info static_tab",
        help_text="Space-separated list of XBlocks on which XBlockAsides should never render in studio",
    )

    @classmethod
    def asides_enabled(cls, block_type):
        """
        Return True if asides are enabled for this type of block in studio
        """
        studio_config = cls.current()
        return studio_config.enabled and block_type not in studio_config.disabled_blocks.split()


class LTIConsumerHideFieldsFlag(ConfigurationModel):
    """
    Disables the editing of "request username" and "request email" fields
    for LTI consumer from the Studio.
    """
    @classmethod
    def lti_access_to_learners_not_editable(cls, course_id):
        """
        Looks at the currently active configuration model to determine whether
        the feature that disables editing of "request username" and "request email"
        fields of LTI consumer is available or not.
        """
        if not LTIConsumerHideFieldsFlag.is_enabled():
            enabled = False
        else:
            effective = (CourseLTIConsumerHideFieldsFlag.objects
                         .filter(course_id=course_id)
                         .order_by('-change_date')
                         .first())
            enabled = effective.enabled if effective is not None else False

        return enabled

    def __unicode__(self):
        current_model = LTIConsumerHideFieldsFlag.current()
        return u"LTIConsumerHideFieldsFlag: enabled {is_enabled}".format(
            is_enabled=current_model.is_enabled(),
        )


class CourseLTIConsumerHideFieldsFlag(ConfigurationModel):
    """
    Disables the editing of "request username" and "request email" fields
    of LTI consumer for a specific course. This only has an effect if
    the general flag of LTIConsumerHideFieldsFlag is set to True.
    """
    KEY_FIELDS = ('course_id',)

    # The course that this feature is attached to.
    course_id = CourseKeyField(max_length=255, db_index=True)

    def __unicode__(self):
        not_en = ""
        if self.enabled:
            not_en = "Not "

        return u"Course '{course_id}': Edit LTI access to Learner information {not_en}Enabled".format(
            course_id=unicode(self.course_id),
            not_en=not_en,
        )
