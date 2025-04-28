(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_nginx"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/nginx.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/nginx.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: Nginx config
Author: Peter Leonov <gojpeg@yandex.ru>
Contributors: Ivan Sagalaev <maniac@softwaremaniacs.org>
Category: common, config
Website: https://www.nginx.com
*/

function nginx(hljs) {
  const VAR = {
    className: 'variable',
    variants: [
      {
        begin: /\$\d+/
      },
      {
        begin: /\$\{/,
        end: /\}/
      },
      {
        begin: /[$@]/ + hljs.UNDERSCORE_IDENT_RE
      }
    ]
  };
  const DEFAULT = {
    endsWithParent: true,
    keywords: {
      $pattern: '[a-z/_]+',
      literal:
        'on off yes no true false none blocked debug info notice warn error crit ' +
        'select break last permanent redirect kqueue rtsig epoll poll /dev/poll'
    },
    relevance: 0,
    illegal: '=>',
    contains: [
      hljs.HASH_COMMENT_MODE,
      {
        className: 'string',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          VAR
        ],
        variants: [
          {
            begin: /"/,
            end: /"/
          },
          {
            begin: /'/,
            end: /'/
          }
        ]
      },
      // this swallows entire URLs to avoid detecting numbers within
      {
        begin: '([a-z]+):/',
        end: '\\s',
        endsWithParent: true,
        excludeEnd: true,
        contains: [ VAR ]
      },
      {
        className: 'regexp',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          VAR
        ],
        variants: [
          {
            begin: "\\s\\^",
            end: "\\s|\\{|;",
            returnEnd: true
          },
          // regexp locations (~, ~*)
          {
            begin: "~\\*?\\s+",
            end: "\\s|\\{|;",
            returnEnd: true
          },
          // *.example.com
          {
            begin: "\\*(\\.[a-z\\-]+)+"
          },
          // sub.example.*
          {
            begin: "([a-z\\-]+\\.)+\\*"
          }
        ]
      },
      // IP
      {
        className: 'number',
        begin: '\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}(:\\d{1,5})?\\b'
      },
      // units
      {
        className: 'number',
        begin: '\\b\\d+[kKmMgGdshdwy]*\\b',
        relevance: 0
      },
      VAR
    ]
  };

  return {
    name: 'Nginx config',
    aliases: [ 'nginxconf' ],
    contains: [
      hljs.HASH_COMMENT_MODE,
      {
        begin: hljs.UNDERSCORE_IDENT_RE + '\\s+\\{',
        returnBegin: true,
        end: /\{/,
        contains: [
          {
            className: 'section',
            begin: hljs.UNDERSCORE_IDENT_RE
          }
        ],
        relevance: 0
      },
      {
        begin: hljs.UNDERSCORE_IDENT_RE + '\\s',
        end: ';|\\{',
        returnBegin: true,
        contains: [
          {
            className: 'attribute',
            begin: hljs.UNDERSCORE_IDENT_RE,
            starts: DEFAULT
          }
        ],
        relevance: 0
      }
    ],
    illegal: '[^\\s\\}]'
  };
}

module.exports = nginx;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbmdpbnguZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0Esb0JBQW9CO0FBQ3BCLGdCQUFnQjtBQUNoQixPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSx5QkFBeUIsRUFBRTtBQUMzQjtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQSx5QkFBeUIsRUFBRTtBQUMzQjtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSx1QkFBdUIsSUFBSSxPQUFPLElBQUksT0FBTyxJQUFJLE9BQU8sSUFBSSxNQUFNLElBQUk7QUFDdEUsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGtEQUFrRDtBQUNsRDtBQUNBLGdCQUFnQjtBQUNoQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsZUFBZSxJQUFJO0FBQ25CO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxzQkFBc0I7QUFDdEI7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvbmdpbnguanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBOZ2lueCBjb25maWdcbkF1dGhvcjogUGV0ZXIgTGVvbm92IDxnb2pwZWdAeWFuZGV4LnJ1PlxuQ29udHJpYnV0b3JzOiBJdmFuIFNhZ2FsYWV2IDxtYW5pYWNAc29mdHdhcmVtYW5pYWNzLm9yZz5cbkNhdGVnb3J5OiBjb21tb24sIGNvbmZpZ1xuV2Vic2l0ZTogaHR0cHM6Ly93d3cubmdpbnguY29tXG4qL1xuXG5mdW5jdGlvbiBuZ2lueChobGpzKSB7XG4gIGNvbnN0IFZBUiA9IHtcbiAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCRcXGQrL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCRcXHsvLFxuICAgICAgICBlbmQ6IC9cXH0vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1skQF0vICsgaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFXG4gICAgICB9XG4gICAgXVxuICB9O1xuICBjb25zdCBERUZBVUxUID0ge1xuICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICAkcGF0dGVybjogJ1thLXovX10rJyxcbiAgICAgIGxpdGVyYWw6XG4gICAgICAgICdvbiBvZmYgeWVzIG5vIHRydWUgZmFsc2Ugbm9uZSBibG9ja2VkIGRlYnVnIGluZm8gbm90aWNlIHdhcm4gZXJyb3IgY3JpdCAnICtcbiAgICAgICAgJ3NlbGVjdCBicmVhayBsYXN0IHBlcm1hbmVudCByZWRpcmVjdCBrcXVldWUgcnRzaWcgZXBvbGwgcG9sbCAvZGV2L3BvbGwnXG4gICAgfSxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgaWxsZWdhbDogJz0+JyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5IQVNIX0NPTU1FTlRfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICAgICAgVkFSXG4gICAgICAgIF0sXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgICAgICBlbmQ6IC9cIi9cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvJy8sXG4gICAgICAgICAgICBlbmQ6IC8nL1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIC8vIHRoaXMgc3dhbGxvd3MgZW50aXJlIFVSTHMgdG8gYXZvaWQgZGV0ZWN0aW5nIG51bWJlcnMgd2l0aGluXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnKFthLXpdKyk6LycsXG4gICAgICAgIGVuZDogJ1xcXFxzJyxcbiAgICAgICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbIFZBUiBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdyZWdleHAnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICBWQVJcbiAgICAgICAgXSxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogXCJcXFxcc1xcXFxeXCIsXG4gICAgICAgICAgICBlbmQ6IFwiXFxcXHN8XFxcXHt8O1wiLFxuICAgICAgICAgICAgcmV0dXJuRW5kOiB0cnVlXG4gICAgICAgICAgfSxcbiAgICAgICAgICAvLyByZWdleHAgbG9jYXRpb25zICh+LCB+KilcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogXCJ+XFxcXCo/XFxcXHMrXCIsXG4gICAgICAgICAgICBlbmQ6IFwiXFxcXHN8XFxcXHt8O1wiLFxuICAgICAgICAgICAgcmV0dXJuRW5kOiB0cnVlXG4gICAgICAgICAgfSxcbiAgICAgICAgICAvLyAqLmV4YW1wbGUuY29tXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IFwiXFxcXCooXFxcXC5bYS16XFxcXC1dKykrXCJcbiAgICAgICAgICB9LFxuICAgICAgICAgIC8vIHN1Yi5leGFtcGxlLipcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogXCIoW2EtelxcXFwtXStcXFxcLikrXFxcXCpcIlxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIC8vIElQXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIGJlZ2luOiAnXFxcXGJcXFxcZHsxLDN9XFxcXC5cXFxcZHsxLDN9XFxcXC5cXFxcZHsxLDN9XFxcXC5cXFxcZHsxLDN9KDpcXFxcZHsxLDV9KT9cXFxcYidcbiAgICAgIH0sXG4gICAgICAvLyB1bml0c1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICBiZWdpbjogJ1xcXFxiXFxcXGQrW2tLbU1nR2RzaGR3eV0qXFxcXGInLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICBWQVJcbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTmdpbnggY29uZmlnJyxcbiAgICBhbGlhc2VzOiBbICduZ2lueGNvbmYnIF0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUgKyAnXFxcXHMrXFxcXHsnLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgZW5kOiAvXFx7LyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdzZWN0aW9uJyxcbiAgICAgICAgICAgIGJlZ2luOiBobGpzLlVOREVSU0NPUkVfSURFTlRfUkVcbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSArICdcXFxccycsXG4gICAgICAgIGVuZDogJzt8XFxcXHsnLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdhdHRyaWJ1dGUnLFxuICAgICAgICAgICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSxcbiAgICAgICAgICAgIHN0YXJ0czogREVGQVVMVFxuICAgICAgICAgIH1cbiAgICAgICAgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9XG4gICAgXSxcbiAgICBpbGxlZ2FsOiAnW15cXFxcc1xcXFx9XSdcbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBuZ2lueDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==