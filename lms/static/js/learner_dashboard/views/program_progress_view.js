(function(define) {
    'use strict';

    define(['backbone',
        'jquery',
        'underscore',
        'gettext',
        'text!../../../templates/learner_dashboard/program_progress_view.underscore',
        'text!../../../templates/learner_dashboard/program_progress_segment.underscore'
    ],
        function(
            Backbone,
            $,
            _,
            gettext,
            programProgressTpl,
            progressSegmentTpl
        ) {
            return Backbone.View.extend({
                x: 22,
                y: 22,
                radius: 16,
                degrees: 180,
                strokeWidth: 1.2,

                viewTpl: _.template(programProgressTpl),
                segmentTpl: _.template(progressSegmentTpl),

                initialize: function(options) {
                    var progress;

                    // Temp. for development
                    this.model = new Backbone.Model({
                        title: options.title || false,
                        label: options.label || false,
                        progress: options.progress || {}
                    });
                    progress = this.model.get('progress');

                    this.model.set({
                        totalCourses: progress.completed + progress.in_progress + progress.not_started
                    });

                    this.render();
                },

                render: function() {
                    var data = $.extend({}, this.model.toJSON(), {
                        circleSegments: this.getProgressSegments(),
                        x: this.x,
                        y: this.y,
                        radius: this.radius,
                        strokeWidth: this.strokeWidth,
                        programData: {
                            type: 'XSeries'
                        }
                    });

                    this.$el.html(this.viewTpl(data));
                },

                getDegreeIncrement: function(total) {
                    return 360 / total;
                },

                getOffset: function(total) {
                    return 100 - ((1 / total) * 100);
                },

                getProgressSegments: function() {
                    var progressHTML = [],
                        total = this.model.get('totalCourses'),
                        segmentDash = 2 * Math.PI * this.radius,
                        degreeInc = this.getDegreeIncrement(total),
                        data = {
                            // Remove strokeWidth to show a gap between
                            dashArray: segmentDash - this.strokeWidth,
                            degrees: this.degrees,
                            offset: this.getOffset(total),
                            x: this.x,
                            y: this.y,
                            radius: this.radius,
                            strokeWidth: this.strokeWidth
                        },
                        i,
                        segmentData;

                    for (i = 0; i < total; i++) {
                        segmentData = $.extend({}, data, {
                            classList: (i >= this.model.get('progress').completed) ? 'incomplete' : 'complete',
                            degrees: data.degrees + (i * degreeInc)
                        });

                        // Want the incomplete segments to have no gaps
                        if (segmentData.classList === 'incomplete' && (i + 1) < total) {
                            segmentData.dashArray = segmentDash;
                        }
                        
                        progressHTML.push(this.segmentTpl(segmentData));
                    }

                    return progressHTML.join('');
                }
            });
        }
    );
}).call(this, define || RequireJS.define);
