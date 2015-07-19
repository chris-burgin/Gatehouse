var pkg = require('./package.json'),
    gulp = require('gulp'),
    rename = require('gulp-rename'),
    autoprefixer = require('gulp-autoprefixer'),
    minify = require('gulp-minify-css'),
    contact = require('gulp-concat');

gulp.task('css', function() {
  return gulp.src('static/*.css')
  .pipe(autoprefixer({
          browsers: ['> 5%'],
          cascade: false
        }))
  .pipe(contact('style.min.css'))
  .pipe(gulp.dest('static/css'))
});

gulp.task('watch', function() {
  gulp.watch('static/*.css', ['css']);
});

gulp.task('default', ['css']);