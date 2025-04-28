(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_dsconfig"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dsconfig.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dsconfig.js ***!
  \***************************************************************************************************/
/***/ ((module) => {

/*
 Language: dsconfig
 Description: dsconfig batch configuration language for LDAP directory servers
 Contributors: Jacob Childress <jacobc@gmail.com>
 Category: enterprise, config
 */

 /** @type LanguageFn */
function dsconfig(hljs) {
  const QUOTED_PROPERTY = {
    className: 'string',
    begin: /"/,
    end: /"/
  };
  const APOS_PROPERTY = {
    className: 'string',
    begin: /'/,
    end: /'/
  };
  const UNQUOTED_PROPERTY = {
    className: 'string',
    begin: /[\w\-?]+:\w+/,
    end: /\W/,
    relevance: 0
  };
  const VALUELESS_PROPERTY = {
    className: 'string',
    begin: /\w+(\-\w+)*/,
    end: /(?=\W)/,
    relevance: 0
  };

  return {
    keywords: 'dsconfig',
    contains: [
      {
        className: 'keyword',
        begin: '^dsconfig',
        end: /\s/,
        excludeEnd: true,
        relevance: 10
      },
      {
        className: 'built_in',
        begin: /(list|create|get|set|delete)-(\w+)/,
        end: /\s/,
        excludeEnd: true,
        illegal: '!@#$%^&*()',
        relevance: 10
      },
      {
        className: 'built_in',
        begin: /--(\w+)/,
        end: /\s/,
        excludeEnd: true
      },
      QUOTED_PROPERTY,
      APOS_PROPERTY,
      UNQUOTED_PROPERTY,
      VALUELESS_PROPERTY,
      hljs.HASH_COMMENT_MODE
    ]
  };
}

module.exports = dsconfig;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZHNjb25maWcuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9kc2NvbmZpZy5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuIExhbmd1YWdlOiBkc2NvbmZpZ1xuIERlc2NyaXB0aW9uOiBkc2NvbmZpZyBiYXRjaCBjb25maWd1cmF0aW9uIGxhbmd1YWdlIGZvciBMREFQIGRpcmVjdG9yeSBzZXJ2ZXJzXG4gQ29udHJpYnV0b3JzOiBKYWNvYiBDaGlsZHJlc3MgPGphY29iY0BnbWFpbC5jb20+XG4gQ2F0ZWdvcnk6IGVudGVycHJpc2UsIGNvbmZpZ1xuICovXG5cbiAvKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gZHNjb25maWcoaGxqcykge1xuICBjb25zdCBRVU9URURfUFJPUEVSVFkgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogL1wiLyxcbiAgICBlbmQ6IC9cIi9cbiAgfTtcbiAgY29uc3QgQVBPU19QUk9QRVJUWSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAvJy8sXG4gICAgZW5kOiAvJy9cbiAgfTtcbiAgY29uc3QgVU5RVU9URURfUFJPUEVSVFkgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogL1tcXHdcXC0/XSs6XFx3Ky8sXG4gICAgZW5kOiAvXFxXLyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgVkFMVUVMRVNTX1BST1BFUlRZID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46IC9cXHcrKFxcLVxcdyspKi8sXG4gICAgZW5kOiAvKD89XFxXKS8sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBrZXl3b3JkczogJ2RzY29uZmlnJyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICAgICAgYmVnaW46ICdeZHNjb25maWcnLFxuICAgICAgICBlbmQ6IC9cXHMvLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdidWlsdF9pbicsXG4gICAgICAgIGJlZ2luOiAvKGxpc3R8Y3JlYXRlfGdldHxzZXR8ZGVsZXRlKS0oXFx3KykvLFxuICAgICAgICBlbmQ6IC9cXHMvLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBpbGxlZ2FsOiAnIUAjJCVeJiooKScsXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2J1aWx0X2luJyxcbiAgICAgICAgYmVnaW46IC8tLShcXHcrKS8sXG4gICAgICAgIGVuZDogL1xccy8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgIH0sXG4gICAgICBRVU9URURfUFJPUEVSVFksXG4gICAgICBBUE9TX1BST1BFUlRZLFxuICAgICAgVU5RVU9URURfUFJPUEVSVFksXG4gICAgICBWQUxVRUxFU1NfUFJPUEVSVFksXG4gICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGRzY29uZmlnO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9