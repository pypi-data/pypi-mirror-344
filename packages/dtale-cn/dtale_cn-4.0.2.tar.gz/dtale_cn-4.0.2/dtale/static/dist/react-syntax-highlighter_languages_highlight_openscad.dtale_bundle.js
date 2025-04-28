(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_openscad"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/openscad.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/openscad.js ***!
  \***************************************************************************************************/
/***/ ((module) => {

/*
Language: OpenSCAD
Author: Dan Panzarella <alsoelp@gmail.com>
Description: OpenSCAD is a language for the 3D CAD modeling software of the same name.
Website: https://www.openscad.org
Category: scientific
*/

function openscad(hljs) {
  const SPECIAL_VARS = {
    className: 'keyword',
    begin: '\\$(f[asn]|t|vp[rtd]|children)'
  };
  const LITERALS = {
    className: 'literal',
    begin: 'false|true|PI|undef'
  };
  const NUMBERS = {
    className: 'number',
    begin: '\\b\\d+(\\.\\d+)?(e-?\\d+)?', // adds 1e5, 1e-10
    relevance: 0
  };
  const STRING = hljs.inherit(hljs.QUOTE_STRING_MODE, {
    illegal: null
  });
  const PREPRO = {
    className: 'meta',
    keywords: {
      'meta-keyword': 'include use'
    },
    begin: 'include|use <',
    end: '>'
  };
  const PARAMS = {
    className: 'params',
    begin: '\\(',
    end: '\\)',
    contains: [
      'self',
      NUMBERS,
      STRING,
      SPECIAL_VARS,
      LITERALS
    ]
  };
  const MODIFIERS = {
    begin: '[*!#%]',
    relevance: 0
  };
  const FUNCTIONS = {
    className: 'function',
    beginKeywords: 'module function',
    end: /=|\{/,
    contains: [
      PARAMS,
      hljs.UNDERSCORE_TITLE_MODE
    ]
  };

  return {
    name: 'OpenSCAD',
    aliases: [ 'scad' ],
    keywords: {
      keyword: 'function module include use for intersection_for if else \\%',
      literal: 'false true PI undef',
      built_in: 'circle square polygon text sphere cube cylinder polyhedron translate rotate scale resize mirror multmatrix color offset hull minkowski union difference intersection abs sign sin cos tan acos asin atan atan2 floor round ceil ln log pow sqrt exp rands min max concat lookup str chr search version version_num norm cross parent_module echo import import_dxf dxf_linear_extrude linear_extrude rotate_extrude surface projection render children dxf_cross dxf_dim let assign'
    },
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      NUMBERS,
      PREPRO,
      STRING,
      SPECIAL_VARS,
      MODIFIERS,
      FUNCTIONS
    ]
  };
}

module.exports = openscad;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfb3BlbnNjYWQuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxjQUFjO0FBQ2Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL29wZW5zY2FkLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogT3BlblNDQURcbkF1dGhvcjogRGFuIFBhbnphcmVsbGEgPGFsc29lbHBAZ21haWwuY29tPlxuRGVzY3JpcHRpb246IE9wZW5TQ0FEIGlzIGEgbGFuZ3VhZ2UgZm9yIHRoZSAzRCBDQUQgbW9kZWxpbmcgc29mdHdhcmUgb2YgdGhlIHNhbWUgbmFtZS5cbldlYnNpdGU6IGh0dHBzOi8vd3d3Lm9wZW5zY2FkLm9yZ1xuQ2F0ZWdvcnk6IHNjaWVudGlmaWNcbiovXG5cbmZ1bmN0aW9uIG9wZW5zY2FkKGhsanMpIHtcbiAgY29uc3QgU1BFQ0lBTF9WQVJTID0ge1xuICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgIGJlZ2luOiAnXFxcXCQoZlthc25dfHR8dnBbcnRkXXxjaGlsZHJlbiknXG4gIH07XG4gIGNvbnN0IExJVEVSQUxTID0ge1xuICAgIGNsYXNzTmFtZTogJ2xpdGVyYWwnLFxuICAgIGJlZ2luOiAnZmFsc2V8dHJ1ZXxQSXx1bmRlZidcbiAgfTtcbiAgY29uc3QgTlVNQkVSUyA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIGJlZ2luOiAnXFxcXGJcXFxcZCsoXFxcXC5cXFxcZCspPyhlLT9cXFxcZCspPycsIC8vIGFkZHMgMWU1LCAxZS0xMFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBTVFJJTkcgPSBobGpzLmluaGVyaXQoaGxqcy5RVU9URV9TVFJJTkdfTU9ERSwge1xuICAgIGlsbGVnYWw6IG51bGxcbiAgfSk7XG4gIGNvbnN0IFBSRVBSTyA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJ21ldGEta2V5d29yZCc6ICdpbmNsdWRlIHVzZSdcbiAgICB9LFxuICAgIGJlZ2luOiAnaW5jbHVkZXx1c2UgPCcsXG4gICAgZW5kOiAnPidcbiAgfTtcbiAgY29uc3QgUEFSQU1TID0ge1xuICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgYmVnaW46ICdcXFxcKCcsXG4gICAgZW5kOiAnXFxcXCknLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICAnc2VsZicsXG4gICAgICBOVU1CRVJTLFxuICAgICAgU1RSSU5HLFxuICAgICAgU1BFQ0lBTF9WQVJTLFxuICAgICAgTElURVJBTFNcbiAgICBdXG4gIH07XG4gIGNvbnN0IE1PRElGSUVSUyA9IHtcbiAgICBiZWdpbjogJ1sqISMlXScsXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIGNvbnN0IEZVTkNUSU9OUyA9IHtcbiAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgYmVnaW5LZXl3b3JkczogJ21vZHVsZSBmdW5jdGlvbicsXG4gICAgZW5kOiAvPXxcXHsvLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBQQVJBTVMsXG4gICAgICBobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERVxuICAgIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdPcGVuU0NBRCcsXG4gICAgYWxpYXNlczogWyAnc2NhZCcgXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDogJ2Z1bmN0aW9uIG1vZHVsZSBpbmNsdWRlIHVzZSBmb3IgaW50ZXJzZWN0aW9uX2ZvciBpZiBlbHNlIFxcXFwlJyxcbiAgICAgIGxpdGVyYWw6ICdmYWxzZSB0cnVlIFBJIHVuZGVmJyxcbiAgICAgIGJ1aWx0X2luOiAnY2lyY2xlIHNxdWFyZSBwb2x5Z29uIHRleHQgc3BoZXJlIGN1YmUgY3lsaW5kZXIgcG9seWhlZHJvbiB0cmFuc2xhdGUgcm90YXRlIHNjYWxlIHJlc2l6ZSBtaXJyb3IgbXVsdG1hdHJpeCBjb2xvciBvZmZzZXQgaHVsbCBtaW5rb3dza2kgdW5pb24gZGlmZmVyZW5jZSBpbnRlcnNlY3Rpb24gYWJzIHNpZ24gc2luIGNvcyB0YW4gYWNvcyBhc2luIGF0YW4gYXRhbjIgZmxvb3Igcm91bmQgY2VpbCBsbiBsb2cgcG93IHNxcnQgZXhwIHJhbmRzIG1pbiBtYXggY29uY2F0IGxvb2t1cCBzdHIgY2hyIHNlYXJjaCB2ZXJzaW9uIHZlcnNpb25fbnVtIG5vcm0gY3Jvc3MgcGFyZW50X21vZHVsZSBlY2hvIGltcG9ydCBpbXBvcnRfZHhmIGR4Zl9saW5lYXJfZXh0cnVkZSBsaW5lYXJfZXh0cnVkZSByb3RhdGVfZXh0cnVkZSBzdXJmYWNlIHByb2plY3Rpb24gcmVuZGVyIGNoaWxkcmVuIGR4Zl9jcm9zcyBkeGZfZGltIGxldCBhc3NpZ24nXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIE5VTUJFUlMsXG4gICAgICBQUkVQUk8sXG4gICAgICBTVFJJTkcsXG4gICAgICBTUEVDSUFMX1ZBUlMsXG4gICAgICBNT0RJRklFUlMsXG4gICAgICBGVU5DVElPTlNcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gb3BlbnNjYWQ7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=