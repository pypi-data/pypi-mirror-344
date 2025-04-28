(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_rsl"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/rsl.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/rsl.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: RenderMan RSL
Author: Konstantin Evdokimenko <qewerty@gmail.com>
Contributors: Shuen-Huei Guan <drake.guan@gmail.com>
Website: https://renderman.pixar.com/resources/RenderMan_20/shadingLanguage.html
Category: graphics
*/

function rsl(hljs) {
  return {
    name: 'RenderMan RSL',
    keywords: {
      keyword:
        'float color point normal vector matrix while for if do return else break extern continue',
      built_in:
        'abs acos ambient area asin atan atmosphere attribute calculatenormal ceil cellnoise ' +
        'clamp comp concat cos degrees depth Deriv diffuse distance Du Dv environment exp ' +
        'faceforward filterstep floor format fresnel incident length lightsource log match ' +
        'max min mod noise normalize ntransform opposite option phong pnoise pow printf ' +
        'ptlined radians random reflect refract renderinfo round setcomp setxcomp setycomp ' +
        'setzcomp shadow sign sin smoothstep specular specularbrdf spline sqrt step tan ' +
        'texture textureinfo trace transform vtransform xcomp ycomp zcomp'
    },
    illegal: '</',
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.APOS_STRING_MODE,
      hljs.C_NUMBER_MODE,
      {
        className: 'meta',
        begin: '#',
        end: '$'
      },
      {
        className: 'class',
        beginKeywords: 'surface displacement light volume imager',
        end: '\\('
      },
      {
        beginKeywords: 'illuminate illuminance gather',
        end: '\\('
      }
    ]
  };
}

module.exports = rsl;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcnNsLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvcnNsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogUmVuZGVyTWFuIFJTTFxuQXV0aG9yOiBLb25zdGFudGluIEV2ZG9raW1lbmtvIDxxZXdlcnR5QGdtYWlsLmNvbT5cbkNvbnRyaWJ1dG9yczogU2h1ZW4tSHVlaSBHdWFuIDxkcmFrZS5ndWFuQGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vcmVuZGVybWFuLnBpeGFyLmNvbS9yZXNvdXJjZXMvUmVuZGVyTWFuXzIwL3NoYWRpbmdMYW5ndWFnZS5odG1sXG5DYXRlZ29yeTogZ3JhcGhpY3NcbiovXG5cbmZ1bmN0aW9uIHJzbChobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1JlbmRlck1hbiBSU0wnLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOlxuICAgICAgICAnZmxvYXQgY29sb3IgcG9pbnQgbm9ybWFsIHZlY3RvciBtYXRyaXggd2hpbGUgZm9yIGlmIGRvIHJldHVybiBlbHNlIGJyZWFrIGV4dGVybiBjb250aW51ZScsXG4gICAgICBidWlsdF9pbjpcbiAgICAgICAgJ2FicyBhY29zIGFtYmllbnQgYXJlYSBhc2luIGF0YW4gYXRtb3NwaGVyZSBhdHRyaWJ1dGUgY2FsY3VsYXRlbm9ybWFsIGNlaWwgY2VsbG5vaXNlICcgK1xuICAgICAgICAnY2xhbXAgY29tcCBjb25jYXQgY29zIGRlZ3JlZXMgZGVwdGggRGVyaXYgZGlmZnVzZSBkaXN0YW5jZSBEdSBEdiBlbnZpcm9ubWVudCBleHAgJyArXG4gICAgICAgICdmYWNlZm9yd2FyZCBmaWx0ZXJzdGVwIGZsb29yIGZvcm1hdCBmcmVzbmVsIGluY2lkZW50IGxlbmd0aCBsaWdodHNvdXJjZSBsb2cgbWF0Y2ggJyArXG4gICAgICAgICdtYXggbWluIG1vZCBub2lzZSBub3JtYWxpemUgbnRyYW5zZm9ybSBvcHBvc2l0ZSBvcHRpb24gcGhvbmcgcG5vaXNlIHBvdyBwcmludGYgJyArXG4gICAgICAgICdwdGxpbmVkIHJhZGlhbnMgcmFuZG9tIHJlZmxlY3QgcmVmcmFjdCByZW5kZXJpbmZvIHJvdW5kIHNldGNvbXAgc2V0eGNvbXAgc2V0eWNvbXAgJyArXG4gICAgICAgICdzZXR6Y29tcCBzaGFkb3cgc2lnbiBzaW4gc21vb3Roc3RlcCBzcGVjdWxhciBzcGVjdWxhcmJyZGYgc3BsaW5lIHNxcnQgc3RlcCB0YW4gJyArXG4gICAgICAgICd0ZXh0dXJlIHRleHR1cmVpbmZvIHRyYWNlIHRyYW5zZm9ybSB2dHJhbnNmb3JtIHhjb21wIHljb21wIHpjb21wJ1xuICAgIH0sXG4gICAgaWxsZWdhbDogJzwvJyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJyMnLFxuICAgICAgICBlbmQ6ICckJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnc3VyZmFjZSBkaXNwbGFjZW1lbnQgbGlnaHQgdm9sdW1lIGltYWdlcicsXG4gICAgICAgIGVuZDogJ1xcXFwoJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2lsbHVtaW5hdGUgaWxsdW1pbmFuY2UgZ2F0aGVyJyxcbiAgICAgICAgZW5kOiAnXFxcXCgnXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHJzbDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==