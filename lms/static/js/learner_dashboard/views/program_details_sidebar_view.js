(function(define) {
    'use strict';

    define(['backbone',
            'jquery',
            'underscore',
            'gettext',
            'js/learner_dashboard/views/program_progress_view',
            'js/learner_dashboard/views/certificate_view',
            'text!../../../templates/learner_dashboard/program_details_sidebar.underscore'
           ],
         function(
             Backbone,
             $,
             _,
             gettext,
             ProgramProgressView,
             CertificateView,
             sidebarTpl
         ) {
             return Backbone.View.extend({
                 tpl: _.template(sidebarTpl),

                 initialize: function(options) {
                     this.courseModel = options.courseModel || {};
                     this.certificateCollection = options.certificateCollection || {};
                     this.render();
                 },

                 render: function() {
                     this.$el.html(this.tpl());
                     this.postRender();
                 },

                 postRender: function() {
console.log(this.model.toJSON());
                     this.newProgramProgressView = new ProgramProgressView({
                         el: '.js-program-progress',
                         title: this.model.get('type') + 'Progress',
                         label: gettext('Earned Certificates'),
                         progress: {
                            completed: this.courseModel.get('completed').length,
                            in_progress: this.courseModel.get('in_progress').length,
                            not_started: this.courseModel.get('not_started').length
                        }
                     });

                     // this.newCertificateView = new CertificateView({
                     //     context: this.context
                     // });
                 }
             });
         }
    );
}).call(this, define || RequireJS.define);
