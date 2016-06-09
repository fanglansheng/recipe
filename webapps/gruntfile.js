'use strict';

module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    // Task configuration goes here.
    sass: {
      main: {
        files: [{
          expand: true,
          cwd: 'recipe/static/recipe/scss',
          src: '**/*.scss',
          dest: 'recipe/static/recipe/css',
          ext: '.css'
        }]
      },
      // deploy: {
      //   options: {
      //     includePaths: ['bower_components/foundation/scss'],
      //     outputStyle: 'compressed'
      //   },
      //   files: {
      //     'build/static/css/screen.min.css': 'myproject/static/scss/screen.scss'
      //   }
      // }
    },

    concurrent: {
      dev: {
        tasks: ['shell:django', 'watch'],
        options: {
          logConcurrentOutput: true
        }
      }
    },

    watch: {
      sass: {
        files: ['recipe/static/recipe/scss/*.scss'],
        tasks: ['sass'],
      },
    },

    shell: {
      options: {
        stderr: false
      },
      django: {
        command: 'python3 manage.py runserver',
        options:{
          stdout:true,
          stderr:true,
          stdin:true,
        }
      },
    }
  });

  // Load plugins here.
  // grunt.loadNpmTasks('grunt-contrib-concat');
  // grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-concurrent');

  // grunt.loadNpmTasks('grunt-contrib-less');
  // grunt.loadNpmTasks('grunt-contrib-watch');

  // Register tasks here.
  grunt.registerTask('default', ['sass:main','concurrent']);

};