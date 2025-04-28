(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_stylus"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/stylus.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/stylus.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

const MODES = (hljs) => {
  return {
    IMPORTANT: {
      className: 'meta',
      begin: '!important'
    },
    HEXCOLOR: {
      className: 'number',
      begin: '#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})'
    },
    ATTRIBUTE_SELECTOR_MODE: {
      className: 'selector-attr',
      begin: /\[/,
      end: /\]/,
      illegal: '$',
      contains: [
        hljs.APOS_STRING_MODE,
        hljs.QUOTE_STRING_MODE
      ]
    }
  };
};

const TAGS = [
  'a',
  'abbr',
  'address',
  'article',
  'aside',
  'audio',
  'b',
  'blockquote',
  'body',
  'button',
  'canvas',
  'caption',
  'cite',
  'code',
  'dd',
  'del',
  'details',
  'dfn',
  'div',
  'dl',
  'dt',
  'em',
  'fieldset',
  'figcaption',
  'figure',
  'footer',
  'form',
  'h1',
  'h2',
  'h3',
  'h4',
  'h5',
  'h6',
  'header',
  'hgroup',
  'html',
  'i',
  'iframe',
  'img',
  'input',
  'ins',
  'kbd',
  'label',
  'legend',
  'li',
  'main',
  'mark',
  'menu',
  'nav',
  'object',
  'ol',
  'p',
  'q',
  'quote',
  'samp',
  'section',
  'span',
  'strong',
  'summary',
  'sup',
  'table',
  'tbody',
  'td',
  'textarea',
  'tfoot',
  'th',
  'thead',
  'time',
  'tr',
  'ul',
  'var',
  'video'
];

const MEDIA_FEATURES = [
  'any-hover',
  'any-pointer',
  'aspect-ratio',
  'color',
  'color-gamut',
  'color-index',
  'device-aspect-ratio',
  'device-height',
  'device-width',
  'display-mode',
  'forced-colors',
  'grid',
  'height',
  'hover',
  'inverted-colors',
  'monochrome',
  'orientation',
  'overflow-block',
  'overflow-inline',
  'pointer',
  'prefers-color-scheme',
  'prefers-contrast',
  'prefers-reduced-motion',
  'prefers-reduced-transparency',
  'resolution',
  'scan',
  'scripting',
  'update',
  'width',
  // TODO: find a better solution?
  'min-width',
  'max-width',
  'min-height',
  'max-height'
];

// https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-classes
const PSEUDO_CLASSES = [
  'active',
  'any-link',
  'blank',
  'checked',
  'current',
  'default',
  'defined',
  'dir', // dir()
  'disabled',
  'drop',
  'empty',
  'enabled',
  'first',
  'first-child',
  'first-of-type',
  'fullscreen',
  'future',
  'focus',
  'focus-visible',
  'focus-within',
  'has', // has()
  'host', // host or host()
  'host-context', // host-context()
  'hover',
  'indeterminate',
  'in-range',
  'invalid',
  'is', // is()
  'lang', // lang()
  'last-child',
  'last-of-type',
  'left',
  'link',
  'local-link',
  'not', // not()
  'nth-child', // nth-child()
  'nth-col', // nth-col()
  'nth-last-child', // nth-last-child()
  'nth-last-col', // nth-last-col()
  'nth-last-of-type', //nth-last-of-type()
  'nth-of-type', //nth-of-type()
  'only-child',
  'only-of-type',
  'optional',
  'out-of-range',
  'past',
  'placeholder-shown',
  'read-only',
  'read-write',
  'required',
  'right',
  'root',
  'scope',
  'target',
  'target-within',
  'user-invalid',
  'valid',
  'visited',
  'where' // where()
];

// https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements
const PSEUDO_ELEMENTS = [
  'after',
  'backdrop',
  'before',
  'cue',
  'cue-region',
  'first-letter',
  'first-line',
  'grammar-error',
  'marker',
  'part',
  'placeholder',
  'selection',
  'slotted',
  'spelling-error'
];

const ATTRIBUTES = [
  'align-content',
  'align-items',
  'align-self',
  'animation',
  'animation-delay',
  'animation-direction',
  'animation-duration',
  'animation-fill-mode',
  'animation-iteration-count',
  'animation-name',
  'animation-play-state',
  'animation-timing-function',
  'auto',
  'backface-visibility',
  'background',
  'background-attachment',
  'background-clip',
  'background-color',
  'background-image',
  'background-origin',
  'background-position',
  'background-repeat',
  'background-size',
  'border',
  'border-bottom',
  'border-bottom-color',
  'border-bottom-left-radius',
  'border-bottom-right-radius',
  'border-bottom-style',
  'border-bottom-width',
  'border-collapse',
  'border-color',
  'border-image',
  'border-image-outset',
  'border-image-repeat',
  'border-image-slice',
  'border-image-source',
  'border-image-width',
  'border-left',
  'border-left-color',
  'border-left-style',
  'border-left-width',
  'border-radius',
  'border-right',
  'border-right-color',
  'border-right-style',
  'border-right-width',
  'border-spacing',
  'border-style',
  'border-top',
  'border-top-color',
  'border-top-left-radius',
  'border-top-right-radius',
  'border-top-style',
  'border-top-width',
  'border-width',
  'bottom',
  'box-decoration-break',
  'box-shadow',
  'box-sizing',
  'break-after',
  'break-before',
  'break-inside',
  'caption-side',
  'clear',
  'clip',
  'clip-path',
  'color',
  'column-count',
  'column-fill',
  'column-gap',
  'column-rule',
  'column-rule-color',
  'column-rule-style',
  'column-rule-width',
  'column-span',
  'column-width',
  'columns',
  'content',
  'counter-increment',
  'counter-reset',
  'cursor',
  'direction',
  'display',
  'empty-cells',
  'filter',
  'flex',
  'flex-basis',
  'flex-direction',
  'flex-flow',
  'flex-grow',
  'flex-shrink',
  'flex-wrap',
  'float',
  'font',
  'font-display',
  'font-family',
  'font-feature-settings',
  'font-kerning',
  'font-language-override',
  'font-size',
  'font-size-adjust',
  'font-smoothing',
  'font-stretch',
  'font-style',
  'font-variant',
  'font-variant-ligatures',
  'font-variation-settings',
  'font-weight',
  'height',
  'hyphens',
  'icon',
  'image-orientation',
  'image-rendering',
  'image-resolution',
  'ime-mode',
  'inherit',
  'initial',
  'justify-content',
  'left',
  'letter-spacing',
  'line-height',
  'list-style',
  'list-style-image',
  'list-style-position',
  'list-style-type',
  'margin',
  'margin-bottom',
  'margin-left',
  'margin-right',
  'margin-top',
  'marks',
  'mask',
  'max-height',
  'max-width',
  'min-height',
  'min-width',
  'nav-down',
  'nav-index',
  'nav-left',
  'nav-right',
  'nav-up',
  'none',
  'normal',
  'object-fit',
  'object-position',
  'opacity',
  'order',
  'orphans',
  'outline',
  'outline-color',
  'outline-offset',
  'outline-style',
  'outline-width',
  'overflow',
  'overflow-wrap',
  'overflow-x',
  'overflow-y',
  'padding',
  'padding-bottom',
  'padding-left',
  'padding-right',
  'padding-top',
  'page-break-after',
  'page-break-before',
  'page-break-inside',
  'perspective',
  'perspective-origin',
  'pointer-events',
  'position',
  'quotes',
  'resize',
  'right',
  'src', // @font-face
  'tab-size',
  'table-layout',
  'text-align',
  'text-align-last',
  'text-decoration',
  'text-decoration-color',
  'text-decoration-line',
  'text-decoration-style',
  'text-indent',
  'text-overflow',
  'text-rendering',
  'text-shadow',
  'text-transform',
  'text-underline-position',
  'top',
  'transform',
  'transform-origin',
  'transform-style',
  'transition',
  'transition-delay',
  'transition-duration',
  'transition-property',
  'transition-timing-function',
  'unicode-bidi',
  'vertical-align',
  'visibility',
  'white-space',
  'widows',
  'width',
  'word-break',
  'word-spacing',
  'word-wrap',
  'z-index'
  // reverse makes sure longer attributes `font-weight` are matched fully
  // instead of getting false positives on say `font`
].reverse();

/*
Language: Stylus
Author: Bryant Williams <b.n.williams@gmail.com>
Description: Stylus is an expressive, robust, feature-rich CSS language built for nodejs.
Website: https://github.com/stylus/stylus
Category: css
*/

/** @type LanguageFn */
function stylus(hljs) {
  const modes = MODES(hljs);

  const AT_MODIFIERS = "and or not only";
  const VARIABLE = {
    className: 'variable',
    begin: '\\$' + hljs.IDENT_RE
  };

  const AT_KEYWORDS = [
    'charset',
    'css',
    'debug',
    'extend',
    'font-face',
    'for',
    'import',
    'include',
    'keyframes',
    'media',
    'mixin',
    'page',
    'warn',
    'while'
  ];

  const LOOKAHEAD_TAG_END = '(?=[.\\s\\n[:,(])';

  // illegals
  const ILLEGAL = [
    '\\?',
    '(\\bReturn\\b)', // monkey
    '(\\bEnd\\b)', // monkey
    '(\\bend\\b)', // vbscript
    '(\\bdef\\b)', // gradle
    ';', // a whole lot of languages
    '#\\s', // markdown
    '\\*\\s', // markdown
    '===\\s', // markdown
    '\\|',
    '%' // prolog
  ];

  return {
    name: 'Stylus',
    aliases: [ 'styl' ],
    case_insensitive: false,
    keywords: 'if else for in',
    illegal: '(' + ILLEGAL.join('|') + ')',
    contains: [

      // strings
      hljs.QUOTE_STRING_MODE,
      hljs.APOS_STRING_MODE,

      // comments
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,

      // hex colors
      modes.HEXCOLOR,

      // class tag
      {
        begin: '\\.[a-zA-Z][a-zA-Z0-9_-]*' + LOOKAHEAD_TAG_END,
        className: 'selector-class'
      },

      // id tag
      {
        begin: '#[a-zA-Z][a-zA-Z0-9_-]*' + LOOKAHEAD_TAG_END,
        className: 'selector-id'
      },

      // tags
      {
        begin: '\\b(' + TAGS.join('|') + ')' + LOOKAHEAD_TAG_END,
        className: 'selector-tag'
      },

      // psuedo selectors
      {
        className: 'selector-pseudo',
        begin: '&?:(' + PSEUDO_CLASSES.join('|') + ')' + LOOKAHEAD_TAG_END
      },
      {
        className: 'selector-pseudo',
        begin: '&?::(' + PSEUDO_ELEMENTS.join('|') + ')' + LOOKAHEAD_TAG_END
      },

      modes.ATTRIBUTE_SELECTOR_MODE,

      {
        className: "keyword",
        begin: /@media/,
        starts: {
          end: /[{;}]/,
          keywords: {
            $pattern: /[a-z-]+/,
            keyword: AT_MODIFIERS,
            attribute: MEDIA_FEATURES.join(" ")
          },
          contains: [ hljs.CSS_NUMBER_MODE ]
        }
      },

      // @ keywords
      {
        className: 'keyword',
        begin: '\@((-(o|moz|ms|webkit)-)?(' + AT_KEYWORDS.join('|') + '))\\b'
      },

      // variables
      VARIABLE,

      // dimension
      hljs.CSS_NUMBER_MODE,

      // functions
      //  - only from beginning of line + whitespace
      {
        className: 'function',
        begin: '^[a-zA-Z][a-zA-Z0-9_\-]*\\(.*\\)',
        illegal: '[\\n]',
        returnBegin: true,
        contains: [
          {
            className: 'title',
            begin: '\\b[a-zA-Z][a-zA-Z0-9_\-]*'
          },
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            contains: [
              modes.HEXCOLOR,
              VARIABLE,
              hljs.APOS_STRING_MODE,
              hljs.CSS_NUMBER_MODE,
              hljs.QUOTE_STRING_MODE
            ]
          }
        ]
      },

      // attributes
      //  - only from beginning of line + whitespace
      //  - must have whitespace after it
      {
        className: 'attribute',
        begin: '\\b(' + ATTRIBUTES.join('|') + ')\\b',
        starts: {
          // value container
          end: /;|$/,
          contains: [
            modes.HEXCOLOR,
            VARIABLE,
            hljs.APOS_STRING_MODE,
            hljs.QUOTE_STRING_MODE,
            hljs.CSS_NUMBER_MODE,
            hljs.C_BLOCK_COMMENT_MODE,
            modes.IMPORTANT
          ],
          illegal: /\./,
          relevance: 0
        }
      }
    ]
  };
}

module.exports = stylus;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc3R5bHVzLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBLDRCQUE0QixFQUFFLGFBQWEsRUFBRTtBQUM3QyxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE1BQU07QUFDTjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTzs7QUFFUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87O0FBRVA7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPOztBQUVQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87O0FBRVA7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxvQkFBb0I7QUFDcEI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLE9BQU87O0FBRVA7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPOztBQUVQO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTzs7QUFFUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9zdHlsdXMuanMiXSwic291cmNlc0NvbnRlbnQiOlsiY29uc3QgTU9ERVMgPSAoaGxqcykgPT4ge1xuICByZXR1cm4ge1xuICAgIElNUE9SVEFOVDoge1xuICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICBiZWdpbjogJyFpbXBvcnRhbnQnXG4gICAgfSxcbiAgICBIRVhDT0xPUjoge1xuICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgIGJlZ2luOiAnIyhbYS1mQS1GMC05XXs2fXxbYS1mQS1GMC05XXszfSknXG4gICAgfSxcbiAgICBBVFRSSUJVVEVfU0VMRUNUT1JfTU9ERToge1xuICAgICAgY2xhc3NOYW1lOiAnc2VsZWN0b3ItYXR0cicsXG4gICAgICBiZWdpbjogL1xcWy8sXG4gICAgICBlbmQ6IC9cXF0vLFxuICAgICAgaWxsZWdhbDogJyQnLFxuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFXG4gICAgICBdXG4gICAgfVxuICB9O1xufTtcblxuY29uc3QgVEFHUyA9IFtcbiAgJ2EnLFxuICAnYWJicicsXG4gICdhZGRyZXNzJyxcbiAgJ2FydGljbGUnLFxuICAnYXNpZGUnLFxuICAnYXVkaW8nLFxuICAnYicsXG4gICdibG9ja3F1b3RlJyxcbiAgJ2JvZHknLFxuICAnYnV0dG9uJyxcbiAgJ2NhbnZhcycsXG4gICdjYXB0aW9uJyxcbiAgJ2NpdGUnLFxuICAnY29kZScsXG4gICdkZCcsXG4gICdkZWwnLFxuICAnZGV0YWlscycsXG4gICdkZm4nLFxuICAnZGl2JyxcbiAgJ2RsJyxcbiAgJ2R0JyxcbiAgJ2VtJyxcbiAgJ2ZpZWxkc2V0JyxcbiAgJ2ZpZ2NhcHRpb24nLFxuICAnZmlndXJlJyxcbiAgJ2Zvb3RlcicsXG4gICdmb3JtJyxcbiAgJ2gxJyxcbiAgJ2gyJyxcbiAgJ2gzJyxcbiAgJ2g0JyxcbiAgJ2g1JyxcbiAgJ2g2JyxcbiAgJ2hlYWRlcicsXG4gICdoZ3JvdXAnLFxuICAnaHRtbCcsXG4gICdpJyxcbiAgJ2lmcmFtZScsXG4gICdpbWcnLFxuICAnaW5wdXQnLFxuICAnaW5zJyxcbiAgJ2tiZCcsXG4gICdsYWJlbCcsXG4gICdsZWdlbmQnLFxuICAnbGknLFxuICAnbWFpbicsXG4gICdtYXJrJyxcbiAgJ21lbnUnLFxuICAnbmF2JyxcbiAgJ29iamVjdCcsXG4gICdvbCcsXG4gICdwJyxcbiAgJ3EnLFxuICAncXVvdGUnLFxuICAnc2FtcCcsXG4gICdzZWN0aW9uJyxcbiAgJ3NwYW4nLFxuICAnc3Ryb25nJyxcbiAgJ3N1bW1hcnknLFxuICAnc3VwJyxcbiAgJ3RhYmxlJyxcbiAgJ3Rib2R5JyxcbiAgJ3RkJyxcbiAgJ3RleHRhcmVhJyxcbiAgJ3Rmb290JyxcbiAgJ3RoJyxcbiAgJ3RoZWFkJyxcbiAgJ3RpbWUnLFxuICAndHInLFxuICAndWwnLFxuICAndmFyJyxcbiAgJ3ZpZGVvJ1xuXTtcblxuY29uc3QgTUVESUFfRkVBVFVSRVMgPSBbXG4gICdhbnktaG92ZXInLFxuICAnYW55LXBvaW50ZXInLFxuICAnYXNwZWN0LXJhdGlvJyxcbiAgJ2NvbG9yJyxcbiAgJ2NvbG9yLWdhbXV0JyxcbiAgJ2NvbG9yLWluZGV4JyxcbiAgJ2RldmljZS1hc3BlY3QtcmF0aW8nLFxuICAnZGV2aWNlLWhlaWdodCcsXG4gICdkZXZpY2Utd2lkdGgnLFxuICAnZGlzcGxheS1tb2RlJyxcbiAgJ2ZvcmNlZC1jb2xvcnMnLFxuICAnZ3JpZCcsXG4gICdoZWlnaHQnLFxuICAnaG92ZXInLFxuICAnaW52ZXJ0ZWQtY29sb3JzJyxcbiAgJ21vbm9jaHJvbWUnLFxuICAnb3JpZW50YXRpb24nLFxuICAnb3ZlcmZsb3ctYmxvY2snLFxuICAnb3ZlcmZsb3ctaW5saW5lJyxcbiAgJ3BvaW50ZXInLFxuICAncHJlZmVycy1jb2xvci1zY2hlbWUnLFxuICAncHJlZmVycy1jb250cmFzdCcsXG4gICdwcmVmZXJzLXJlZHVjZWQtbW90aW9uJyxcbiAgJ3ByZWZlcnMtcmVkdWNlZC10cmFuc3BhcmVuY3knLFxuICAncmVzb2x1dGlvbicsXG4gICdzY2FuJyxcbiAgJ3NjcmlwdGluZycsXG4gICd1cGRhdGUnLFxuICAnd2lkdGgnLFxuICAvLyBUT0RPOiBmaW5kIGEgYmV0dGVyIHNvbHV0aW9uP1xuICAnbWluLXdpZHRoJyxcbiAgJ21heC13aWR0aCcsXG4gICdtaW4taGVpZ2h0JyxcbiAgJ21heC1oZWlnaHQnXG5dO1xuXG4vLyBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi1VUy9kb2NzL1dlYi9DU1MvUHNldWRvLWNsYXNzZXNcbmNvbnN0IFBTRVVET19DTEFTU0VTID0gW1xuICAnYWN0aXZlJyxcbiAgJ2FueS1saW5rJyxcbiAgJ2JsYW5rJyxcbiAgJ2NoZWNrZWQnLFxuICAnY3VycmVudCcsXG4gICdkZWZhdWx0JyxcbiAgJ2RlZmluZWQnLFxuICAnZGlyJywgLy8gZGlyKClcbiAgJ2Rpc2FibGVkJyxcbiAgJ2Ryb3AnLFxuICAnZW1wdHknLFxuICAnZW5hYmxlZCcsXG4gICdmaXJzdCcsXG4gICdmaXJzdC1jaGlsZCcsXG4gICdmaXJzdC1vZi10eXBlJyxcbiAgJ2Z1bGxzY3JlZW4nLFxuICAnZnV0dXJlJyxcbiAgJ2ZvY3VzJyxcbiAgJ2ZvY3VzLXZpc2libGUnLFxuICAnZm9jdXMtd2l0aGluJyxcbiAgJ2hhcycsIC8vIGhhcygpXG4gICdob3N0JywgLy8gaG9zdCBvciBob3N0KClcbiAgJ2hvc3QtY29udGV4dCcsIC8vIGhvc3QtY29udGV4dCgpXG4gICdob3ZlcicsXG4gICdpbmRldGVybWluYXRlJyxcbiAgJ2luLXJhbmdlJyxcbiAgJ2ludmFsaWQnLFxuICAnaXMnLCAvLyBpcygpXG4gICdsYW5nJywgLy8gbGFuZygpXG4gICdsYXN0LWNoaWxkJyxcbiAgJ2xhc3Qtb2YtdHlwZScsXG4gICdsZWZ0JyxcbiAgJ2xpbmsnLFxuICAnbG9jYWwtbGluaycsXG4gICdub3QnLCAvLyBub3QoKVxuICAnbnRoLWNoaWxkJywgLy8gbnRoLWNoaWxkKClcbiAgJ250aC1jb2wnLCAvLyBudGgtY29sKClcbiAgJ250aC1sYXN0LWNoaWxkJywgLy8gbnRoLWxhc3QtY2hpbGQoKVxuICAnbnRoLWxhc3QtY29sJywgLy8gbnRoLWxhc3QtY29sKClcbiAgJ250aC1sYXN0LW9mLXR5cGUnLCAvL250aC1sYXN0LW9mLXR5cGUoKVxuICAnbnRoLW9mLXR5cGUnLCAvL250aC1vZi10eXBlKClcbiAgJ29ubHktY2hpbGQnLFxuICAnb25seS1vZi10eXBlJyxcbiAgJ29wdGlvbmFsJyxcbiAgJ291dC1vZi1yYW5nZScsXG4gICdwYXN0JyxcbiAgJ3BsYWNlaG9sZGVyLXNob3duJyxcbiAgJ3JlYWQtb25seScsXG4gICdyZWFkLXdyaXRlJyxcbiAgJ3JlcXVpcmVkJyxcbiAgJ3JpZ2h0JyxcbiAgJ3Jvb3QnLFxuICAnc2NvcGUnLFxuICAndGFyZ2V0JyxcbiAgJ3RhcmdldC13aXRoaW4nLFxuICAndXNlci1pbnZhbGlkJyxcbiAgJ3ZhbGlkJyxcbiAgJ3Zpc2l0ZWQnLFxuICAnd2hlcmUnIC8vIHdoZXJlKClcbl07XG5cbi8vIGh0dHBzOi8vZGV2ZWxvcGVyLm1vemlsbGEub3JnL2VuLVVTL2RvY3MvV2ViL0NTUy9Qc2V1ZG8tZWxlbWVudHNcbmNvbnN0IFBTRVVET19FTEVNRU5UUyA9IFtcbiAgJ2FmdGVyJyxcbiAgJ2JhY2tkcm9wJyxcbiAgJ2JlZm9yZScsXG4gICdjdWUnLFxuICAnY3VlLXJlZ2lvbicsXG4gICdmaXJzdC1sZXR0ZXInLFxuICAnZmlyc3QtbGluZScsXG4gICdncmFtbWFyLWVycm9yJyxcbiAgJ21hcmtlcicsXG4gICdwYXJ0JyxcbiAgJ3BsYWNlaG9sZGVyJyxcbiAgJ3NlbGVjdGlvbicsXG4gICdzbG90dGVkJyxcbiAgJ3NwZWxsaW5nLWVycm9yJ1xuXTtcblxuY29uc3QgQVRUUklCVVRFUyA9IFtcbiAgJ2FsaWduLWNvbnRlbnQnLFxuICAnYWxpZ24taXRlbXMnLFxuICAnYWxpZ24tc2VsZicsXG4gICdhbmltYXRpb24nLFxuICAnYW5pbWF0aW9uLWRlbGF5JyxcbiAgJ2FuaW1hdGlvbi1kaXJlY3Rpb24nLFxuICAnYW5pbWF0aW9uLWR1cmF0aW9uJyxcbiAgJ2FuaW1hdGlvbi1maWxsLW1vZGUnLFxuICAnYW5pbWF0aW9uLWl0ZXJhdGlvbi1jb3VudCcsXG4gICdhbmltYXRpb24tbmFtZScsXG4gICdhbmltYXRpb24tcGxheS1zdGF0ZScsXG4gICdhbmltYXRpb24tdGltaW5nLWZ1bmN0aW9uJyxcbiAgJ2F1dG8nLFxuICAnYmFja2ZhY2UtdmlzaWJpbGl0eScsXG4gICdiYWNrZ3JvdW5kJyxcbiAgJ2JhY2tncm91bmQtYXR0YWNobWVudCcsXG4gICdiYWNrZ3JvdW5kLWNsaXAnLFxuICAnYmFja2dyb3VuZC1jb2xvcicsXG4gICdiYWNrZ3JvdW5kLWltYWdlJyxcbiAgJ2JhY2tncm91bmQtb3JpZ2luJyxcbiAgJ2JhY2tncm91bmQtcG9zaXRpb24nLFxuICAnYmFja2dyb3VuZC1yZXBlYXQnLFxuICAnYmFja2dyb3VuZC1zaXplJyxcbiAgJ2JvcmRlcicsXG4gICdib3JkZXItYm90dG9tJyxcbiAgJ2JvcmRlci1ib3R0b20tY29sb3InLFxuICAnYm9yZGVyLWJvdHRvbS1sZWZ0LXJhZGl1cycsXG4gICdib3JkZXItYm90dG9tLXJpZ2h0LXJhZGl1cycsXG4gICdib3JkZXItYm90dG9tLXN0eWxlJyxcbiAgJ2JvcmRlci1ib3R0b20td2lkdGgnLFxuICAnYm9yZGVyLWNvbGxhcHNlJyxcbiAgJ2JvcmRlci1jb2xvcicsXG4gICdib3JkZXItaW1hZ2UnLFxuICAnYm9yZGVyLWltYWdlLW91dHNldCcsXG4gICdib3JkZXItaW1hZ2UtcmVwZWF0JyxcbiAgJ2JvcmRlci1pbWFnZS1zbGljZScsXG4gICdib3JkZXItaW1hZ2Utc291cmNlJyxcbiAgJ2JvcmRlci1pbWFnZS13aWR0aCcsXG4gICdib3JkZXItbGVmdCcsXG4gICdib3JkZXItbGVmdC1jb2xvcicsXG4gICdib3JkZXItbGVmdC1zdHlsZScsXG4gICdib3JkZXItbGVmdC13aWR0aCcsXG4gICdib3JkZXItcmFkaXVzJyxcbiAgJ2JvcmRlci1yaWdodCcsXG4gICdib3JkZXItcmlnaHQtY29sb3InLFxuICAnYm9yZGVyLXJpZ2h0LXN0eWxlJyxcbiAgJ2JvcmRlci1yaWdodC13aWR0aCcsXG4gICdib3JkZXItc3BhY2luZycsXG4gICdib3JkZXItc3R5bGUnLFxuICAnYm9yZGVyLXRvcCcsXG4gICdib3JkZXItdG9wLWNvbG9yJyxcbiAgJ2JvcmRlci10b3AtbGVmdC1yYWRpdXMnLFxuICAnYm9yZGVyLXRvcC1yaWdodC1yYWRpdXMnLFxuICAnYm9yZGVyLXRvcC1zdHlsZScsXG4gICdib3JkZXItdG9wLXdpZHRoJyxcbiAgJ2JvcmRlci13aWR0aCcsXG4gICdib3R0b20nLFxuICAnYm94LWRlY29yYXRpb24tYnJlYWsnLFxuICAnYm94LXNoYWRvdycsXG4gICdib3gtc2l6aW5nJyxcbiAgJ2JyZWFrLWFmdGVyJyxcbiAgJ2JyZWFrLWJlZm9yZScsXG4gICdicmVhay1pbnNpZGUnLFxuICAnY2FwdGlvbi1zaWRlJyxcbiAgJ2NsZWFyJyxcbiAgJ2NsaXAnLFxuICAnY2xpcC1wYXRoJyxcbiAgJ2NvbG9yJyxcbiAgJ2NvbHVtbi1jb3VudCcsXG4gICdjb2x1bW4tZmlsbCcsXG4gICdjb2x1bW4tZ2FwJyxcbiAgJ2NvbHVtbi1ydWxlJyxcbiAgJ2NvbHVtbi1ydWxlLWNvbG9yJyxcbiAgJ2NvbHVtbi1ydWxlLXN0eWxlJyxcbiAgJ2NvbHVtbi1ydWxlLXdpZHRoJyxcbiAgJ2NvbHVtbi1zcGFuJyxcbiAgJ2NvbHVtbi13aWR0aCcsXG4gICdjb2x1bW5zJyxcbiAgJ2NvbnRlbnQnLFxuICAnY291bnRlci1pbmNyZW1lbnQnLFxuICAnY291bnRlci1yZXNldCcsXG4gICdjdXJzb3InLFxuICAnZGlyZWN0aW9uJyxcbiAgJ2Rpc3BsYXknLFxuICAnZW1wdHktY2VsbHMnLFxuICAnZmlsdGVyJyxcbiAgJ2ZsZXgnLFxuICAnZmxleC1iYXNpcycsXG4gICdmbGV4LWRpcmVjdGlvbicsXG4gICdmbGV4LWZsb3cnLFxuICAnZmxleC1ncm93JyxcbiAgJ2ZsZXgtc2hyaW5rJyxcbiAgJ2ZsZXgtd3JhcCcsXG4gICdmbG9hdCcsXG4gICdmb250JyxcbiAgJ2ZvbnQtZGlzcGxheScsXG4gICdmb250LWZhbWlseScsXG4gICdmb250LWZlYXR1cmUtc2V0dGluZ3MnLFxuICAnZm9udC1rZXJuaW5nJyxcbiAgJ2ZvbnQtbGFuZ3VhZ2Utb3ZlcnJpZGUnLFxuICAnZm9udC1zaXplJyxcbiAgJ2ZvbnQtc2l6ZS1hZGp1c3QnLFxuICAnZm9udC1zbW9vdGhpbmcnLFxuICAnZm9udC1zdHJldGNoJyxcbiAgJ2ZvbnQtc3R5bGUnLFxuICAnZm9udC12YXJpYW50JyxcbiAgJ2ZvbnQtdmFyaWFudC1saWdhdHVyZXMnLFxuICAnZm9udC12YXJpYXRpb24tc2V0dGluZ3MnLFxuICAnZm9udC13ZWlnaHQnLFxuICAnaGVpZ2h0JyxcbiAgJ2h5cGhlbnMnLFxuICAnaWNvbicsXG4gICdpbWFnZS1vcmllbnRhdGlvbicsXG4gICdpbWFnZS1yZW5kZXJpbmcnLFxuICAnaW1hZ2UtcmVzb2x1dGlvbicsXG4gICdpbWUtbW9kZScsXG4gICdpbmhlcml0JyxcbiAgJ2luaXRpYWwnLFxuICAnanVzdGlmeS1jb250ZW50JyxcbiAgJ2xlZnQnLFxuICAnbGV0dGVyLXNwYWNpbmcnLFxuICAnbGluZS1oZWlnaHQnLFxuICAnbGlzdC1zdHlsZScsXG4gICdsaXN0LXN0eWxlLWltYWdlJyxcbiAgJ2xpc3Qtc3R5bGUtcG9zaXRpb24nLFxuICAnbGlzdC1zdHlsZS10eXBlJyxcbiAgJ21hcmdpbicsXG4gICdtYXJnaW4tYm90dG9tJyxcbiAgJ21hcmdpbi1sZWZ0JyxcbiAgJ21hcmdpbi1yaWdodCcsXG4gICdtYXJnaW4tdG9wJyxcbiAgJ21hcmtzJyxcbiAgJ21hc2snLFxuICAnbWF4LWhlaWdodCcsXG4gICdtYXgtd2lkdGgnLFxuICAnbWluLWhlaWdodCcsXG4gICdtaW4td2lkdGgnLFxuICAnbmF2LWRvd24nLFxuICAnbmF2LWluZGV4JyxcbiAgJ25hdi1sZWZ0JyxcbiAgJ25hdi1yaWdodCcsXG4gICduYXYtdXAnLFxuICAnbm9uZScsXG4gICdub3JtYWwnLFxuICAnb2JqZWN0LWZpdCcsXG4gICdvYmplY3QtcG9zaXRpb24nLFxuICAnb3BhY2l0eScsXG4gICdvcmRlcicsXG4gICdvcnBoYW5zJyxcbiAgJ291dGxpbmUnLFxuICAnb3V0bGluZS1jb2xvcicsXG4gICdvdXRsaW5lLW9mZnNldCcsXG4gICdvdXRsaW5lLXN0eWxlJyxcbiAgJ291dGxpbmUtd2lkdGgnLFxuICAnb3ZlcmZsb3cnLFxuICAnb3ZlcmZsb3ctd3JhcCcsXG4gICdvdmVyZmxvdy14JyxcbiAgJ292ZXJmbG93LXknLFxuICAncGFkZGluZycsXG4gICdwYWRkaW5nLWJvdHRvbScsXG4gICdwYWRkaW5nLWxlZnQnLFxuICAncGFkZGluZy1yaWdodCcsXG4gICdwYWRkaW5nLXRvcCcsXG4gICdwYWdlLWJyZWFrLWFmdGVyJyxcbiAgJ3BhZ2UtYnJlYWstYmVmb3JlJyxcbiAgJ3BhZ2UtYnJlYWstaW5zaWRlJyxcbiAgJ3BlcnNwZWN0aXZlJyxcbiAgJ3BlcnNwZWN0aXZlLW9yaWdpbicsXG4gICdwb2ludGVyLWV2ZW50cycsXG4gICdwb3NpdGlvbicsXG4gICdxdW90ZXMnLFxuICAncmVzaXplJyxcbiAgJ3JpZ2h0JyxcbiAgJ3NyYycsIC8vIEBmb250LWZhY2VcbiAgJ3RhYi1zaXplJyxcbiAgJ3RhYmxlLWxheW91dCcsXG4gICd0ZXh0LWFsaWduJyxcbiAgJ3RleHQtYWxpZ24tbGFzdCcsXG4gICd0ZXh0LWRlY29yYXRpb24nLFxuICAndGV4dC1kZWNvcmF0aW9uLWNvbG9yJyxcbiAgJ3RleHQtZGVjb3JhdGlvbi1saW5lJyxcbiAgJ3RleHQtZGVjb3JhdGlvbi1zdHlsZScsXG4gICd0ZXh0LWluZGVudCcsXG4gICd0ZXh0LW92ZXJmbG93JyxcbiAgJ3RleHQtcmVuZGVyaW5nJyxcbiAgJ3RleHQtc2hhZG93JyxcbiAgJ3RleHQtdHJhbnNmb3JtJyxcbiAgJ3RleHQtdW5kZXJsaW5lLXBvc2l0aW9uJyxcbiAgJ3RvcCcsXG4gICd0cmFuc2Zvcm0nLFxuICAndHJhbnNmb3JtLW9yaWdpbicsXG4gICd0cmFuc2Zvcm0tc3R5bGUnLFxuICAndHJhbnNpdGlvbicsXG4gICd0cmFuc2l0aW9uLWRlbGF5JyxcbiAgJ3RyYW5zaXRpb24tZHVyYXRpb24nLFxuICAndHJhbnNpdGlvbi1wcm9wZXJ0eScsXG4gICd0cmFuc2l0aW9uLXRpbWluZy1mdW5jdGlvbicsXG4gICd1bmljb2RlLWJpZGknLFxuICAndmVydGljYWwtYWxpZ24nLFxuICAndmlzaWJpbGl0eScsXG4gICd3aGl0ZS1zcGFjZScsXG4gICd3aWRvd3MnLFxuICAnd2lkdGgnLFxuICAnd29yZC1icmVhaycsXG4gICd3b3JkLXNwYWNpbmcnLFxuICAnd29yZC13cmFwJyxcbiAgJ3otaW5kZXgnXG4gIC8vIHJldmVyc2UgbWFrZXMgc3VyZSBsb25nZXIgYXR0cmlidXRlcyBgZm9udC13ZWlnaHRgIGFyZSBtYXRjaGVkIGZ1bGx5XG4gIC8vIGluc3RlYWQgb2YgZ2V0dGluZyBmYWxzZSBwb3NpdGl2ZXMgb24gc2F5IGBmb250YFxuXS5yZXZlcnNlKCk7XG5cbi8qXG5MYW5ndWFnZTogU3R5bHVzXG5BdXRob3I6IEJyeWFudCBXaWxsaWFtcyA8Yi5uLndpbGxpYW1zQGdtYWlsLmNvbT5cbkRlc2NyaXB0aW9uOiBTdHlsdXMgaXMgYW4gZXhwcmVzc2l2ZSwgcm9idXN0LCBmZWF0dXJlLXJpY2ggQ1NTIGxhbmd1YWdlIGJ1aWx0IGZvciBub2RlanMuXG5XZWJzaXRlOiBodHRwczovL2dpdGh1Yi5jb20vc3R5bHVzL3N0eWx1c1xuQ2F0ZWdvcnk6IGNzc1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIHN0eWx1cyhobGpzKSB7XG4gIGNvbnN0IG1vZGVzID0gTU9ERVMoaGxqcyk7XG5cbiAgY29uc3QgQVRfTU9ESUZJRVJTID0gXCJhbmQgb3Igbm90IG9ubHlcIjtcbiAgY29uc3QgVkFSSUFCTEUgPSB7XG4gICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgIGJlZ2luOiAnXFxcXCQnICsgaGxqcy5JREVOVF9SRVxuICB9O1xuXG4gIGNvbnN0IEFUX0tFWVdPUkRTID0gW1xuICAgICdjaGFyc2V0JyxcbiAgICAnY3NzJyxcbiAgICAnZGVidWcnLFxuICAgICdleHRlbmQnLFxuICAgICdmb250LWZhY2UnLFxuICAgICdmb3InLFxuICAgICdpbXBvcnQnLFxuICAgICdpbmNsdWRlJyxcbiAgICAna2V5ZnJhbWVzJyxcbiAgICAnbWVkaWEnLFxuICAgICdtaXhpbicsXG4gICAgJ3BhZ2UnLFxuICAgICd3YXJuJyxcbiAgICAnd2hpbGUnXG4gIF07XG5cbiAgY29uc3QgTE9PS0FIRUFEX1RBR19FTkQgPSAnKD89Wy5cXFxcc1xcXFxuWzosKF0pJztcblxuICAvLyBpbGxlZ2Fsc1xuICBjb25zdCBJTExFR0FMID0gW1xuICAgICdcXFxcPycsXG4gICAgJyhcXFxcYlJldHVyblxcXFxiKScsIC8vIG1vbmtleVxuICAgICcoXFxcXGJFbmRcXFxcYiknLCAvLyBtb25rZXlcbiAgICAnKFxcXFxiZW5kXFxcXGIpJywgLy8gdmJzY3JpcHRcbiAgICAnKFxcXFxiZGVmXFxcXGIpJywgLy8gZ3JhZGxlXG4gICAgJzsnLCAvLyBhIHdob2xlIGxvdCBvZiBsYW5ndWFnZXNcbiAgICAnI1xcXFxzJywgLy8gbWFya2Rvd25cbiAgICAnXFxcXCpcXFxccycsIC8vIG1hcmtkb3duXG4gICAgJz09PVxcXFxzJywgLy8gbWFya2Rvd25cbiAgICAnXFxcXHwnLFxuICAgICclJyAvLyBwcm9sb2dcbiAgXTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdTdHlsdXMnLFxuICAgIGFsaWFzZXM6IFsgJ3N0eWwnIF0sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogZmFsc2UsXG4gICAga2V5d29yZHM6ICdpZiBlbHNlIGZvciBpbicsXG4gICAgaWxsZWdhbDogJygnICsgSUxMRUdBTC5qb2luKCd8JykgKyAnKScsXG4gICAgY29udGFpbnM6IFtcblxuICAgICAgLy8gc3RyaW5nc1xuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcblxuICAgICAgLy8gY29tbWVudHNcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG5cbiAgICAgIC8vIGhleCBjb2xvcnNcbiAgICAgIG1vZGVzLkhFWENPTE9SLFxuXG4gICAgICAvLyBjbGFzcyB0YWdcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXFxcLlthLXpBLVpdW2EtekEtWjAtOV8tXSonICsgTE9PS0FIRUFEX1RBR19FTkQsXG4gICAgICAgIGNsYXNzTmFtZTogJ3NlbGVjdG9yLWNsYXNzJ1xuICAgICAgfSxcblxuICAgICAgLy8gaWQgdGFnXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnI1thLXpBLVpdW2EtekEtWjAtOV8tXSonICsgTE9PS0FIRUFEX1RBR19FTkQsXG4gICAgICAgIGNsYXNzTmFtZTogJ3NlbGVjdG9yLWlkJ1xuICAgICAgfSxcblxuICAgICAgLy8gdGFnc1xuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFxiKCcgKyBUQUdTLmpvaW4oJ3wnKSArICcpJyArIExPT0tBSEVBRF9UQUdfRU5ELFxuICAgICAgICBjbGFzc05hbWU6ICdzZWxlY3Rvci10YWcnXG4gICAgICB9LFxuXG4gICAgICAvLyBwc3VlZG8gc2VsZWN0b3JzXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3NlbGVjdG9yLXBzZXVkbycsXG4gICAgICAgIGJlZ2luOiAnJj86KCcgKyBQU0VVRE9fQ0xBU1NFUy5qb2luKCd8JykgKyAnKScgKyBMT09LQUhFQURfVEFHX0VORFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc2VsZWN0b3ItcHNldWRvJyxcbiAgICAgICAgYmVnaW46ICcmPzo6KCcgKyBQU0VVRE9fRUxFTUVOVFMuam9pbignfCcpICsgJyknICsgTE9PS0FIRUFEX1RBR19FTkRcbiAgICAgIH0sXG5cbiAgICAgIG1vZGVzLkFUVFJJQlVURV9TRUxFQ1RPUl9NT0RFLFxuXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogXCJrZXl3b3JkXCIsXG4gICAgICAgIGJlZ2luOiAvQG1lZGlhLyxcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgZW5kOiAvW3s7fV0vLFxuICAgICAgICAgIGtleXdvcmRzOiB7XG4gICAgICAgICAgICAkcGF0dGVybjogL1thLXotXSsvLFxuICAgICAgICAgICAga2V5d29yZDogQVRfTU9ESUZJRVJTLFxuICAgICAgICAgICAgYXR0cmlidXRlOiBNRURJQV9GRUFUVVJFUy5qb2luKFwiIFwiKVxuICAgICAgICAgIH0sXG4gICAgICAgICAgY29udGFpbnM6IFsgaGxqcy5DU1NfTlVNQkVSX01PREUgXVxuICAgICAgICB9XG4gICAgICB9LFxuXG4gICAgICAvLyBAIGtleXdvcmRzXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgICAgICBiZWdpbjogJ1xcQCgoLShvfG1venxtc3x3ZWJraXQpLSk/KCcgKyBBVF9LRVlXT1JEUy5qb2luKCd8JykgKyAnKSlcXFxcYidcbiAgICAgIH0sXG5cbiAgICAgIC8vIHZhcmlhYmxlc1xuICAgICAgVkFSSUFCTEUsXG5cbiAgICAgIC8vIGRpbWVuc2lvblxuICAgICAgaGxqcy5DU1NfTlVNQkVSX01PREUsXG5cbiAgICAgIC8vIGZ1bmN0aW9uc1xuICAgICAgLy8gIC0gb25seSBmcm9tIGJlZ2lubmluZyBvZiBsaW5lICsgd2hpdGVzcGFjZVxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luOiAnXlthLXpBLVpdW2EtekEtWjAtOV9cXC1dKlxcXFwoLipcXFxcKScsXG4gICAgICAgIGlsbGVnYWw6ICdbXFxcXG5dJyxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAndGl0bGUnLFxuICAgICAgICAgICAgYmVnaW46ICdcXFxcYlthLXpBLVpdW2EtekEtWjAtOV9cXC1dKidcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICBiZWdpbjogL1xcKC8sXG4gICAgICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgbW9kZXMuSEVYQ09MT1IsXG4gICAgICAgICAgICAgIFZBUklBQkxFLFxuICAgICAgICAgICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICAgICAgICAgIGhsanMuQ1NTX05VTUJFUl9NT0RFLFxuICAgICAgICAgICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFXG4gICAgICAgICAgICBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuXG4gICAgICAvLyBhdHRyaWJ1dGVzXG4gICAgICAvLyAgLSBvbmx5IGZyb20gYmVnaW5uaW5nIG9mIGxpbmUgKyB3aGl0ZXNwYWNlXG4gICAgICAvLyAgLSBtdXN0IGhhdmUgd2hpdGVzcGFjZSBhZnRlciBpdFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdhdHRyaWJ1dGUnLFxuICAgICAgICBiZWdpbjogJ1xcXFxiKCcgKyBBVFRSSUJVVEVTLmpvaW4oJ3wnKSArICcpXFxcXGInLFxuICAgICAgICBzdGFydHM6IHtcbiAgICAgICAgICAvLyB2YWx1ZSBjb250YWluZXJcbiAgICAgICAgICBlbmQ6IC87fCQvLFxuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICBtb2Rlcy5IRVhDT0xPUixcbiAgICAgICAgICAgIFZBUklBQkxFLFxuICAgICAgICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgICAgICAgIGhsanMuQ1NTX05VTUJFUl9NT0RFLFxuICAgICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICAgIG1vZGVzLklNUE9SVEFOVFxuICAgICAgICAgIF0sXG4gICAgICAgICAgaWxsZWdhbDogL1xcLi8sXG4gICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgIH1cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gc3R5bHVzO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9