(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_django"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/django.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/django.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Django
Description: Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
Requires: xml.js
Author: Ivan Sagalaev <maniac@softwaremaniacs.org>
Contributors: Ilya Baryshev <baryshev@gmail.com>
Website: https://www.djangoproject.com
Category: template
*/

/** @type LanguageFn */
function django(hljs) {
  const FILTER = {
    begin: /\|[A-Za-z]+:?/,
    keywords: {
      name:
        'truncatewords removetags linebreaksbr yesno get_digit timesince random striptags ' +
        'filesizeformat escape linebreaks length_is ljust rjust cut urlize fix_ampersands ' +
        'title floatformat capfirst pprint divisibleby add make_list unordered_list urlencode ' +
        'timeuntil urlizetrunc wordcount stringformat linenumbers slice date dictsort ' +
        'dictsortreversed default_if_none pluralize lower join center default ' +
        'truncatewords_html upper length phone2numeric wordwrap time addslashes slugify first ' +
        'escapejs force_escape iriencode last safe safeseq truncatechars localize unlocalize ' +
        'localtime utc timezone'
    },
    contains: [
      hljs.QUOTE_STRING_MODE,
      hljs.APOS_STRING_MODE
    ]
  };

  return {
    name: 'Django',
    aliases: ['jinja'],
    case_insensitive: true,
    subLanguage: 'xml',
    contains: [
      hljs.COMMENT(/\{%\s*comment\s*%\}/, /\{%\s*endcomment\s*%\}/),
      hljs.COMMENT(/\{#/, /#\}/),
      {
        className: 'template-tag',
        begin: /\{%/,
        end: /%\}/,
        contains: [{
          className: 'name',
          begin: /\w+/,
          keywords: {
            name:
                'comment endcomment load templatetag ifchanged endifchanged if endif firstof for ' +
                'endfor ifnotequal endifnotequal widthratio extends include spaceless ' +
                'endspaceless regroup ifequal endifequal ssi now with cycle url filter ' +
                'endfilter debug block endblock else autoescape endautoescape csrf_token empty elif ' +
                'endwith static trans blocktrans endblocktrans get_static_prefix get_media_prefix ' +
                'plural get_current_language language get_available_languages ' +
                'get_current_language_bidi get_language_info get_language_info_list localize ' +
                'endlocalize localtime endlocaltime timezone endtimezone get_current_timezone ' +
                'verbatim'
          },
          starts: {
            endsWithParent: true,
            keywords: 'in by as',
            contains: [FILTER],
            relevance: 0
          }
        }]
      },
      {
        className: 'template-variable',
        begin: /\{\{/,
        end: /\}\}/,
        contains: [FILTER]
      }
    ]
  };
}

module.exports = django;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZGphbmdvLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esc0JBQXNCLGlCQUFpQixNQUFNLG9CQUFvQjtBQUNqRSxzQkFBc0IsUUFBUTtBQUM5QjtBQUNBO0FBQ0Esa0JBQWtCO0FBQ2xCLGlCQUFpQjtBQUNqQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVCxPQUFPO0FBQ1A7QUFDQTtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLGdCQUFnQixFQUFFO0FBQ2xCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2RqYW5nby5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IERqYW5nb1xuRGVzY3JpcHRpb246IERqYW5nbyBpcyBhIGhpZ2gtbGV2ZWwgUHl0aG9uIFdlYiBmcmFtZXdvcmsgdGhhdCBlbmNvdXJhZ2VzIHJhcGlkIGRldmVsb3BtZW50IGFuZCBjbGVhbiwgcHJhZ21hdGljIGRlc2lnbi5cblJlcXVpcmVzOiB4bWwuanNcbkF1dGhvcjogSXZhbiBTYWdhbGFldiA8bWFuaWFjQHNvZnR3YXJlbWFuaWFjcy5vcmc+XG5Db250cmlidXRvcnM6IElseWEgQmFyeXNoZXYgPGJhcnlzaGV2QGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vd3d3LmRqYW5nb3Byb2plY3QuY29tXG5DYXRlZ29yeTogdGVtcGxhdGVcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBkamFuZ28oaGxqcykge1xuICBjb25zdCBGSUxURVIgPSB7XG4gICAgYmVnaW46IC9cXHxbQS1aYS16XSs6Py8sXG4gICAga2V5d29yZHM6IHtcbiAgICAgIG5hbWU6XG4gICAgICAgICd0cnVuY2F0ZXdvcmRzIHJlbW92ZXRhZ3MgbGluZWJyZWFrc2JyIHllc25vIGdldF9kaWdpdCB0aW1lc2luY2UgcmFuZG9tIHN0cmlwdGFncyAnICtcbiAgICAgICAgJ2ZpbGVzaXplZm9ybWF0IGVzY2FwZSBsaW5lYnJlYWtzIGxlbmd0aF9pcyBsanVzdCByanVzdCBjdXQgdXJsaXplIGZpeF9hbXBlcnNhbmRzICcgK1xuICAgICAgICAndGl0bGUgZmxvYXRmb3JtYXQgY2FwZmlyc3QgcHByaW50IGRpdmlzaWJsZWJ5IGFkZCBtYWtlX2xpc3QgdW5vcmRlcmVkX2xpc3QgdXJsZW5jb2RlICcgK1xuICAgICAgICAndGltZXVudGlsIHVybGl6ZXRydW5jIHdvcmRjb3VudCBzdHJpbmdmb3JtYXQgbGluZW51bWJlcnMgc2xpY2UgZGF0ZSBkaWN0c29ydCAnICtcbiAgICAgICAgJ2RpY3Rzb3J0cmV2ZXJzZWQgZGVmYXVsdF9pZl9ub25lIHBsdXJhbGl6ZSBsb3dlciBqb2luIGNlbnRlciBkZWZhdWx0ICcgK1xuICAgICAgICAndHJ1bmNhdGV3b3Jkc19odG1sIHVwcGVyIGxlbmd0aCBwaG9uZTJudW1lcmljIHdvcmR3cmFwIHRpbWUgYWRkc2xhc2hlcyBzbHVnaWZ5IGZpcnN0ICcgK1xuICAgICAgICAnZXNjYXBlanMgZm9yY2VfZXNjYXBlIGlyaWVuY29kZSBsYXN0IHNhZmUgc2FmZXNlcSB0cnVuY2F0ZWNoYXJzIGxvY2FsaXplIHVubG9jYWxpemUgJyArXG4gICAgICAgICdsb2NhbHRpbWUgdXRjIHRpbWV6b25lJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREVcbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnRGphbmdvJyxcbiAgICBhbGlhc2VzOiBbJ2ppbmphJ10sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBzdWJMYW5ndWFnZTogJ3htbCcsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ09NTUVOVCgvXFx7JVxccypjb21tZW50XFxzKiVcXH0vLCAvXFx7JVxccyplbmRjb21tZW50XFxzKiVcXH0vKSxcbiAgICAgIGhsanMuQ09NTUVOVCgvXFx7Iy8sIC8jXFx9LyksXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RlbXBsYXRlLXRhZycsXG4gICAgICAgIGJlZ2luOiAvXFx7JS8sXG4gICAgICAgIGVuZDogLyVcXH0vLFxuICAgICAgICBjb250YWluczogW3tcbiAgICAgICAgICBjbGFzc05hbWU6ICduYW1lJyxcbiAgICAgICAgICBiZWdpbjogL1xcdysvLFxuICAgICAgICAgIGtleXdvcmRzOiB7XG4gICAgICAgICAgICBuYW1lOlxuICAgICAgICAgICAgICAgICdjb21tZW50IGVuZGNvbW1lbnQgbG9hZCB0ZW1wbGF0ZXRhZyBpZmNoYW5nZWQgZW5kaWZjaGFuZ2VkIGlmIGVuZGlmIGZpcnN0b2YgZm9yICcgK1xuICAgICAgICAgICAgICAgICdlbmRmb3IgaWZub3RlcXVhbCBlbmRpZm5vdGVxdWFsIHdpZHRocmF0aW8gZXh0ZW5kcyBpbmNsdWRlIHNwYWNlbGVzcyAnICtcbiAgICAgICAgICAgICAgICAnZW5kc3BhY2VsZXNzIHJlZ3JvdXAgaWZlcXVhbCBlbmRpZmVxdWFsIHNzaSBub3cgd2l0aCBjeWNsZSB1cmwgZmlsdGVyICcgK1xuICAgICAgICAgICAgICAgICdlbmRmaWx0ZXIgZGVidWcgYmxvY2sgZW5kYmxvY2sgZWxzZSBhdXRvZXNjYXBlIGVuZGF1dG9lc2NhcGUgY3NyZl90b2tlbiBlbXB0eSBlbGlmICcgK1xuICAgICAgICAgICAgICAgICdlbmR3aXRoIHN0YXRpYyB0cmFucyBibG9ja3RyYW5zIGVuZGJsb2NrdHJhbnMgZ2V0X3N0YXRpY19wcmVmaXggZ2V0X21lZGlhX3ByZWZpeCAnICtcbiAgICAgICAgICAgICAgICAncGx1cmFsIGdldF9jdXJyZW50X2xhbmd1YWdlIGxhbmd1YWdlIGdldF9hdmFpbGFibGVfbGFuZ3VhZ2VzICcgK1xuICAgICAgICAgICAgICAgICdnZXRfY3VycmVudF9sYW5ndWFnZV9iaWRpIGdldF9sYW5ndWFnZV9pbmZvIGdldF9sYW5ndWFnZV9pbmZvX2xpc3QgbG9jYWxpemUgJyArXG4gICAgICAgICAgICAgICAgJ2VuZGxvY2FsaXplIGxvY2FsdGltZSBlbmRsb2NhbHRpbWUgdGltZXpvbmUgZW5kdGltZXpvbmUgZ2V0X2N1cnJlbnRfdGltZXpvbmUgJyArXG4gICAgICAgICAgICAgICAgJ3ZlcmJhdGltJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgICAgIGtleXdvcmRzOiAnaW4gYnkgYXMnLFxuICAgICAgICAgICAgY29udGFpbnM6IFtGSUxURVJdLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfVxuICAgICAgICB9XVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdmFyaWFibGUnLFxuICAgICAgICBiZWdpbjogL1xce1xcey8sXG4gICAgICAgIGVuZDogL1xcfVxcfS8sXG4gICAgICAgIGNvbnRhaW5zOiBbRklMVEVSXVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBkamFuZ287XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=