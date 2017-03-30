"""
Django admin dashboard configuration for LMS XBlock infrastructure.
"""

from django.contrib import admin
from config_models.admin import ConfigurationModelAdmin, KeyedConfigurationModelAdmin

from xblock_config.forms import CourseLTIConsumerHideFieldsAdminForm
from xblock_config.models import (
    CourseLTIConsumerHideFieldsFlag,
    LTIConsumerHideFieldsFlag,
    StudioConfig,
)


class CourseLTIConsumerHideFieldsFlagAdmin(KeyedConfigurationModelAdmin):
    """
    Admin for feature(i.e. hiding the LTI fields) on course-by-course basis.
    Allows searching by course id.
    """
    form = CourseLTIConsumerHideFieldsAdminForm
    search_fields = ['course_id']
    fieldsets = (
        (None, {
            'fields': ('course_id', 'enabled'),
            'description': 'Enter a valid course id. If it is invalid, an error message will be displayed.'
        }),
    )

admin.site.register(StudioConfig, ConfigurationModelAdmin)
admin.site.register(LTIConsumerHideFieldsFlag, ConfigurationModelAdmin)
admin.site.register(CourseLTIConsumerHideFieldsFlag, CourseLTIConsumerHideFieldsFlagAdmin)
