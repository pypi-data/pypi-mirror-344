(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_diff"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/diff.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/diff.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Diff
Description: Unified and context diff
Author: Vasily Polovnyov <vast@whiteants.net>
Website: https://www.gnu.org/software/diffutils/
Category: common
*/

/** @type LanguageFn */
function diff(hljs) {
  return {
    name: 'Diff',
    aliases: ['patch'],
    contains: [
      {
        className: 'meta',
        relevance: 10,
        variants: [
          {
            begin: /^@@ +-\d+,\d+ +\+\d+,\d+ +@@/
          },
          {
            begin: /^\*\*\* +\d+,\d+ +\*\*\*\*$/
          },
          {
            begin: /^--- +\d+,\d+ +----$/
          }
        ]
      },
      {
        className: 'comment',
        variants: [
          {
            begin: /Index: /,
            end: /$/
          },
          {
            begin: /^index/,
            end: /$/
          },
          {
            begin: /={3,}/,
            end: /$/
          },
          {
            begin: /^-{3}/,
            end: /$/
          },
          {
            begin: /^\*{3} /,
            end: /$/
          },
          {
            begin: /^\+{3}/,
            end: /$/
          },
          {
            begin: /^\*{15}$/
          },
          {
            begin: /^diff --git/,
            end: /$/
          }
        ]
      },
      {
        className: 'addition',
        begin: /^\+/,
        end: /$/
      },
      {
        className: 'deletion',
        begin: /^-/,
        end: /$/
      },
      {
        className: 'addition',
        begin: /^!/,
        end: /$/
      }
    ]
  };
}

module.exports = diff;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZGlmZi5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0Esc0JBQXNCLEdBQUc7QUFDekI7QUFDQSxXQUFXO0FBQ1g7QUFDQSx1QkFBdUIsRUFBRTtBQUN6QjtBQUNBLFdBQVc7QUFDWDtBQUNBLHdCQUF3QixHQUFHO0FBQzNCO0FBQ0EsV0FBVztBQUNYO0FBQ0Esd0JBQXdCLEVBQUU7QUFDMUI7QUFDQSxXQUFXO0FBQ1g7QUFDQSx3QkFBd0IsR0FBRztBQUMzQixXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9kaWZmLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogRGlmZlxuRGVzY3JpcHRpb246IFVuaWZpZWQgYW5kIGNvbnRleHQgZGlmZlxuQXV0aG9yOiBWYXNpbHkgUG9sb3ZueW92IDx2YXN0QHdoaXRlYW50cy5uZXQ+XG5XZWJzaXRlOiBodHRwczovL3d3dy5nbnUub3JnL3NvZnR3YXJlL2RpZmZ1dGlscy9cbkNhdGVnb3J5OiBjb21tb25cbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBkaWZmKGhsanMpIHtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnRGlmZicsXG4gICAgYWxpYXNlczogWydwYXRjaCddLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICByZWxldmFuY2U6IDEwLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXkBAICstXFxkKyxcXGQrICtcXCtcXGQrLFxcZCsgK0BAL1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9eXFwqXFwqXFwqICtcXGQrLFxcZCsgK1xcKlxcKlxcKlxcKiQvXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL14tLS0gK1xcZCssXFxkKyArLS0tLSQvXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjb21tZW50JyxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL0luZGV4OiAvLFxuICAgICAgICAgICAgZW5kOiAvJC9cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXmluZGV4LyxcbiAgICAgICAgICAgIGVuZDogLyQvXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogLz17Myx9LyxcbiAgICAgICAgICAgIGVuZDogLyQvXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL14tezN9LyxcbiAgICAgICAgICAgIGVuZDogLyQvXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL15cXCp7M30gLyxcbiAgICAgICAgICAgIGVuZDogLyQvXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL15cXCt7M30vLFxuICAgICAgICAgICAgZW5kOiAvJC9cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXlxcKnsxNX0kL1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9eZGlmZiAtLWdpdC8sXG4gICAgICAgICAgICBlbmQ6IC8kL1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnYWRkaXRpb24nLFxuICAgICAgICBiZWdpbjogL15cXCsvLFxuICAgICAgICBlbmQ6IC8kL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZGVsZXRpb24nLFxuICAgICAgICBiZWdpbjogL14tLyxcbiAgICAgICAgZW5kOiAvJC9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2FkZGl0aW9uJyxcbiAgICAgICAgYmVnaW46IC9eIS8sXG4gICAgICAgIGVuZDogLyQvXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGRpZmY7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=