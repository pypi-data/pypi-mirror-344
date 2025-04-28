(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_css"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/css.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/css.js ***!
  \**********************************************************************************************/
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

/**
 * @param {string} value
 * @returns {RegExp}
 * */

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function source(re) {
  if (!re) return null;
  if (typeof re === "string") return re;

  return re.source;
}

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function lookahead(re) {
  return concat('(?=', re, ')');
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/*
Language: CSS
Category: common, css
Website: https://developer.mozilla.org/en-US/docs/Web/CSS
*/

/** @type LanguageFn */
function css(hljs) {
  const modes = MODES(hljs);
  const FUNCTION_DISPATCH = {
    className: "built_in",
    begin: /[\w-]+(?=\()/
  };
  const VENDOR_PREFIX = {
    begin: /-(webkit|moz|ms|o)-(?=[a-z])/
  };
  const AT_MODIFIERS = "and or not only";
  const AT_PROPERTY_RE = /@-?\w[\w]*(-\w+)*/; // @-webkit-keyframes
  const IDENT_RE = '[a-zA-Z-][a-zA-Z0-9_-]*';
  const STRINGS = [
    hljs.APOS_STRING_MODE,
    hljs.QUOTE_STRING_MODE
  ];

  return {
    name: 'CSS',
    case_insensitive: true,
    illegal: /[=|'\$]/,
    keywords: {
      keyframePosition: "from to"
    },
    classNameAliases: {
      // for visual continuity with `tag {}` and because we
      // don't have a great class for this?
      keyframePosition: "selector-tag"
    },
    contains: [
      hljs.C_BLOCK_COMMENT_MODE,
      VENDOR_PREFIX,
      // to recognize keyframe 40% etc which are outside the scope of our
      // attribute value mode
      hljs.CSS_NUMBER_MODE,
      {
        className: 'selector-id',
        begin: /#[A-Za-z0-9_-]+/,
        relevance: 0
      },
      {
        className: 'selector-class',
        begin: '\\.' + IDENT_RE,
        relevance: 0
      },
      modes.ATTRIBUTE_SELECTOR_MODE,
      {
        className: 'selector-pseudo',
        variants: [
          {
            begin: ':(' + PSEUDO_CLASSES.join('|') + ')'
          },
          {
            begin: '::(' + PSEUDO_ELEMENTS.join('|') + ')'
          }
        ]
      },
      // we may actually need this (12/2020)
      // { // pseudo-selector params
      //   begin: /\(/,
      //   end: /\)/,
      //   contains: [ hljs.CSS_NUMBER_MODE ]
      // },
      {
        className: 'attribute',
        begin: '\\b(' + ATTRIBUTES.join('|') + ')\\b'
      },
      // attribute values
      {
        begin: ':',
        end: '[;}]',
        contains: [
          modes.HEXCOLOR,
          modes.IMPORTANT,
          hljs.CSS_NUMBER_MODE,
          ...STRINGS,
          // needed to highlight these as strings and to avoid issues with
          // illegal characters that might be inside urls that would tigger the
          // languages illegal stack
          {
            begin: /(url|data-uri)\(/,
            end: /\)/,
            relevance: 0, // from keywords
            keywords: {
              built_in: "url data-uri"
            },
            contains: [
              {
                className: "string",
                // any character other than `)` as in `url()` will be the start
                // of a string, which ends with `)` (from the parent mode)
                begin: /[^)]/,
                endsWithParent: true,
                excludeEnd: true
              }
            ]
          },
          FUNCTION_DISPATCH
        ]
      },
      {
        begin: lookahead(/@/),
        end: '[{;]',
        relevance: 0,
        illegal: /:/, // break on Less variables @var: ...
        contains: [
          {
            className: 'keyword',
            begin: AT_PROPERTY_RE
          },
          {
            begin: /\s/,
            endsWithParent: true,
            excludeEnd: true,
            relevance: 0,
            keywords: {
              $pattern: /[a-z-]+/,
              keyword: AT_MODIFIERS,
              attribute: MEDIA_FEATURES.join(" ")
            },
            contains: [
              {
                begin: /[a-z-]+(?=:)/,
                className: "attribute"
              },
              ...STRINGS,
              hljs.CSS_NUMBER_MODE
            ]
          }
        ]
      },
      {
        className: 'selector-tag',
        begin: '\\b(' + TAGS.join('|') + ')\\b'
      }
    ]
  };
}

module.exports = css;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY3NzLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBLDRCQUE0QixFQUFFLGFBQWEsRUFBRTtBQUM3QyxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDhDQUE4QztBQUM5QztBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBLDJDQUEyQztBQUMzQztBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQSxVQUFVO0FBQ1Y7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2Nzcy5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJjb25zdCBNT0RFUyA9IChobGpzKSA9PiB7XG4gIHJldHVybiB7XG4gICAgSU1QT1JUQU5UOiB7XG4gICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgIGJlZ2luOiAnIWltcG9ydGFudCdcbiAgICB9LFxuICAgIEhFWENPTE9SOiB7XG4gICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgYmVnaW46ICcjKFthLWZBLUYwLTldezZ9fFthLWZBLUYwLTldezN9KSdcbiAgICB9LFxuICAgIEFUVFJJQlVURV9TRUxFQ1RPUl9NT0RFOiB7XG4gICAgICBjbGFzc05hbWU6ICdzZWxlY3Rvci1hdHRyJyxcbiAgICAgIGJlZ2luOiAvXFxbLyxcbiAgICAgIGVuZDogL1xcXS8sXG4gICAgICBpbGxlZ2FsOiAnJCcsXG4gICAgICBjb250YWluczogW1xuICAgICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREVcbiAgICAgIF1cbiAgICB9XG4gIH07XG59O1xuXG5jb25zdCBUQUdTID0gW1xuICAnYScsXG4gICdhYmJyJyxcbiAgJ2FkZHJlc3MnLFxuICAnYXJ0aWNsZScsXG4gICdhc2lkZScsXG4gICdhdWRpbycsXG4gICdiJyxcbiAgJ2Jsb2NrcXVvdGUnLFxuICAnYm9keScsXG4gICdidXR0b24nLFxuICAnY2FudmFzJyxcbiAgJ2NhcHRpb24nLFxuICAnY2l0ZScsXG4gICdjb2RlJyxcbiAgJ2RkJyxcbiAgJ2RlbCcsXG4gICdkZXRhaWxzJyxcbiAgJ2RmbicsXG4gICdkaXYnLFxuICAnZGwnLFxuICAnZHQnLFxuICAnZW0nLFxuICAnZmllbGRzZXQnLFxuICAnZmlnY2FwdGlvbicsXG4gICdmaWd1cmUnLFxuICAnZm9vdGVyJyxcbiAgJ2Zvcm0nLFxuICAnaDEnLFxuICAnaDInLFxuICAnaDMnLFxuICAnaDQnLFxuICAnaDUnLFxuICAnaDYnLFxuICAnaGVhZGVyJyxcbiAgJ2hncm91cCcsXG4gICdodG1sJyxcbiAgJ2knLFxuICAnaWZyYW1lJyxcbiAgJ2ltZycsXG4gICdpbnB1dCcsXG4gICdpbnMnLFxuICAna2JkJyxcbiAgJ2xhYmVsJyxcbiAgJ2xlZ2VuZCcsXG4gICdsaScsXG4gICdtYWluJyxcbiAgJ21hcmsnLFxuICAnbWVudScsXG4gICduYXYnLFxuICAnb2JqZWN0JyxcbiAgJ29sJyxcbiAgJ3AnLFxuICAncScsXG4gICdxdW90ZScsXG4gICdzYW1wJyxcbiAgJ3NlY3Rpb24nLFxuICAnc3BhbicsXG4gICdzdHJvbmcnLFxuICAnc3VtbWFyeScsXG4gICdzdXAnLFxuICAndGFibGUnLFxuICAndGJvZHknLFxuICAndGQnLFxuICAndGV4dGFyZWEnLFxuICAndGZvb3QnLFxuICAndGgnLFxuICAndGhlYWQnLFxuICAndGltZScsXG4gICd0cicsXG4gICd1bCcsXG4gICd2YXInLFxuICAndmlkZW8nXG5dO1xuXG5jb25zdCBNRURJQV9GRUFUVVJFUyA9IFtcbiAgJ2FueS1ob3ZlcicsXG4gICdhbnktcG9pbnRlcicsXG4gICdhc3BlY3QtcmF0aW8nLFxuICAnY29sb3InLFxuICAnY29sb3ItZ2FtdXQnLFxuICAnY29sb3ItaW5kZXgnLFxuICAnZGV2aWNlLWFzcGVjdC1yYXRpbycsXG4gICdkZXZpY2UtaGVpZ2h0JyxcbiAgJ2RldmljZS13aWR0aCcsXG4gICdkaXNwbGF5LW1vZGUnLFxuICAnZm9yY2VkLWNvbG9ycycsXG4gICdncmlkJyxcbiAgJ2hlaWdodCcsXG4gICdob3ZlcicsXG4gICdpbnZlcnRlZC1jb2xvcnMnLFxuICAnbW9ub2Nocm9tZScsXG4gICdvcmllbnRhdGlvbicsXG4gICdvdmVyZmxvdy1ibG9jaycsXG4gICdvdmVyZmxvdy1pbmxpbmUnLFxuICAncG9pbnRlcicsXG4gICdwcmVmZXJzLWNvbG9yLXNjaGVtZScsXG4gICdwcmVmZXJzLWNvbnRyYXN0JyxcbiAgJ3ByZWZlcnMtcmVkdWNlZC1tb3Rpb24nLFxuICAncHJlZmVycy1yZWR1Y2VkLXRyYW5zcGFyZW5jeScsXG4gICdyZXNvbHV0aW9uJyxcbiAgJ3NjYW4nLFxuICAnc2NyaXB0aW5nJyxcbiAgJ3VwZGF0ZScsXG4gICd3aWR0aCcsXG4gIC8vIFRPRE86IGZpbmQgYSBiZXR0ZXIgc29sdXRpb24/XG4gICdtaW4td2lkdGgnLFxuICAnbWF4LXdpZHRoJyxcbiAgJ21pbi1oZWlnaHQnLFxuICAnbWF4LWhlaWdodCdcbl07XG5cbi8vIGh0dHBzOi8vZGV2ZWxvcGVyLm1vemlsbGEub3JnL2VuLVVTL2RvY3MvV2ViL0NTUy9Qc2V1ZG8tY2xhc3Nlc1xuY29uc3QgUFNFVURPX0NMQVNTRVMgPSBbXG4gICdhY3RpdmUnLFxuICAnYW55LWxpbmsnLFxuICAnYmxhbmsnLFxuICAnY2hlY2tlZCcsXG4gICdjdXJyZW50JyxcbiAgJ2RlZmF1bHQnLFxuICAnZGVmaW5lZCcsXG4gICdkaXInLCAvLyBkaXIoKVxuICAnZGlzYWJsZWQnLFxuICAnZHJvcCcsXG4gICdlbXB0eScsXG4gICdlbmFibGVkJyxcbiAgJ2ZpcnN0JyxcbiAgJ2ZpcnN0LWNoaWxkJyxcbiAgJ2ZpcnN0LW9mLXR5cGUnLFxuICAnZnVsbHNjcmVlbicsXG4gICdmdXR1cmUnLFxuICAnZm9jdXMnLFxuICAnZm9jdXMtdmlzaWJsZScsXG4gICdmb2N1cy13aXRoaW4nLFxuICAnaGFzJywgLy8gaGFzKClcbiAgJ2hvc3QnLCAvLyBob3N0IG9yIGhvc3QoKVxuICAnaG9zdC1jb250ZXh0JywgLy8gaG9zdC1jb250ZXh0KClcbiAgJ2hvdmVyJyxcbiAgJ2luZGV0ZXJtaW5hdGUnLFxuICAnaW4tcmFuZ2UnLFxuICAnaW52YWxpZCcsXG4gICdpcycsIC8vIGlzKClcbiAgJ2xhbmcnLCAvLyBsYW5nKClcbiAgJ2xhc3QtY2hpbGQnLFxuICAnbGFzdC1vZi10eXBlJyxcbiAgJ2xlZnQnLFxuICAnbGluaycsXG4gICdsb2NhbC1saW5rJyxcbiAgJ25vdCcsIC8vIG5vdCgpXG4gICdudGgtY2hpbGQnLCAvLyBudGgtY2hpbGQoKVxuICAnbnRoLWNvbCcsIC8vIG50aC1jb2woKVxuICAnbnRoLWxhc3QtY2hpbGQnLCAvLyBudGgtbGFzdC1jaGlsZCgpXG4gICdudGgtbGFzdC1jb2wnLCAvLyBudGgtbGFzdC1jb2woKVxuICAnbnRoLWxhc3Qtb2YtdHlwZScsIC8vbnRoLWxhc3Qtb2YtdHlwZSgpXG4gICdudGgtb2YtdHlwZScsIC8vbnRoLW9mLXR5cGUoKVxuICAnb25seS1jaGlsZCcsXG4gICdvbmx5LW9mLXR5cGUnLFxuICAnb3B0aW9uYWwnLFxuICAnb3V0LW9mLXJhbmdlJyxcbiAgJ3Bhc3QnLFxuICAncGxhY2Vob2xkZXItc2hvd24nLFxuICAncmVhZC1vbmx5JyxcbiAgJ3JlYWQtd3JpdGUnLFxuICAncmVxdWlyZWQnLFxuICAncmlnaHQnLFxuICAncm9vdCcsXG4gICdzY29wZScsXG4gICd0YXJnZXQnLFxuICAndGFyZ2V0LXdpdGhpbicsXG4gICd1c2VyLWludmFsaWQnLFxuICAndmFsaWQnLFxuICAndmlzaXRlZCcsXG4gICd3aGVyZScgLy8gd2hlcmUoKVxuXTtcblxuLy8gaHR0cHM6Ly9kZXZlbG9wZXIubW96aWxsYS5vcmcvZW4tVVMvZG9jcy9XZWIvQ1NTL1BzZXVkby1lbGVtZW50c1xuY29uc3QgUFNFVURPX0VMRU1FTlRTID0gW1xuICAnYWZ0ZXInLFxuICAnYmFja2Ryb3AnLFxuICAnYmVmb3JlJyxcbiAgJ2N1ZScsXG4gICdjdWUtcmVnaW9uJyxcbiAgJ2ZpcnN0LWxldHRlcicsXG4gICdmaXJzdC1saW5lJyxcbiAgJ2dyYW1tYXItZXJyb3InLFxuICAnbWFya2VyJyxcbiAgJ3BhcnQnLFxuICAncGxhY2Vob2xkZXInLFxuICAnc2VsZWN0aW9uJyxcbiAgJ3Nsb3R0ZWQnLFxuICAnc3BlbGxpbmctZXJyb3InXG5dO1xuXG5jb25zdCBBVFRSSUJVVEVTID0gW1xuICAnYWxpZ24tY29udGVudCcsXG4gICdhbGlnbi1pdGVtcycsXG4gICdhbGlnbi1zZWxmJyxcbiAgJ2FuaW1hdGlvbicsXG4gICdhbmltYXRpb24tZGVsYXknLFxuICAnYW5pbWF0aW9uLWRpcmVjdGlvbicsXG4gICdhbmltYXRpb24tZHVyYXRpb24nLFxuICAnYW5pbWF0aW9uLWZpbGwtbW9kZScsXG4gICdhbmltYXRpb24taXRlcmF0aW9uLWNvdW50JyxcbiAgJ2FuaW1hdGlvbi1uYW1lJyxcbiAgJ2FuaW1hdGlvbi1wbGF5LXN0YXRlJyxcbiAgJ2FuaW1hdGlvbi10aW1pbmctZnVuY3Rpb24nLFxuICAnYXV0bycsXG4gICdiYWNrZmFjZS12aXNpYmlsaXR5JyxcbiAgJ2JhY2tncm91bmQnLFxuICAnYmFja2dyb3VuZC1hdHRhY2htZW50JyxcbiAgJ2JhY2tncm91bmQtY2xpcCcsXG4gICdiYWNrZ3JvdW5kLWNvbG9yJyxcbiAgJ2JhY2tncm91bmQtaW1hZ2UnLFxuICAnYmFja2dyb3VuZC1vcmlnaW4nLFxuICAnYmFja2dyb3VuZC1wb3NpdGlvbicsXG4gICdiYWNrZ3JvdW5kLXJlcGVhdCcsXG4gICdiYWNrZ3JvdW5kLXNpemUnLFxuICAnYm9yZGVyJyxcbiAgJ2JvcmRlci1ib3R0b20nLFxuICAnYm9yZGVyLWJvdHRvbS1jb2xvcicsXG4gICdib3JkZXItYm90dG9tLWxlZnQtcmFkaXVzJyxcbiAgJ2JvcmRlci1ib3R0b20tcmlnaHQtcmFkaXVzJyxcbiAgJ2JvcmRlci1ib3R0b20tc3R5bGUnLFxuICAnYm9yZGVyLWJvdHRvbS13aWR0aCcsXG4gICdib3JkZXItY29sbGFwc2UnLFxuICAnYm9yZGVyLWNvbG9yJyxcbiAgJ2JvcmRlci1pbWFnZScsXG4gICdib3JkZXItaW1hZ2Utb3V0c2V0JyxcbiAgJ2JvcmRlci1pbWFnZS1yZXBlYXQnLFxuICAnYm9yZGVyLWltYWdlLXNsaWNlJyxcbiAgJ2JvcmRlci1pbWFnZS1zb3VyY2UnLFxuICAnYm9yZGVyLWltYWdlLXdpZHRoJyxcbiAgJ2JvcmRlci1sZWZ0JyxcbiAgJ2JvcmRlci1sZWZ0LWNvbG9yJyxcbiAgJ2JvcmRlci1sZWZ0LXN0eWxlJyxcbiAgJ2JvcmRlci1sZWZ0LXdpZHRoJyxcbiAgJ2JvcmRlci1yYWRpdXMnLFxuICAnYm9yZGVyLXJpZ2h0JyxcbiAgJ2JvcmRlci1yaWdodC1jb2xvcicsXG4gICdib3JkZXItcmlnaHQtc3R5bGUnLFxuICAnYm9yZGVyLXJpZ2h0LXdpZHRoJyxcbiAgJ2JvcmRlci1zcGFjaW5nJyxcbiAgJ2JvcmRlci1zdHlsZScsXG4gICdib3JkZXItdG9wJyxcbiAgJ2JvcmRlci10b3AtY29sb3InLFxuICAnYm9yZGVyLXRvcC1sZWZ0LXJhZGl1cycsXG4gICdib3JkZXItdG9wLXJpZ2h0LXJhZGl1cycsXG4gICdib3JkZXItdG9wLXN0eWxlJyxcbiAgJ2JvcmRlci10b3Atd2lkdGgnLFxuICAnYm9yZGVyLXdpZHRoJyxcbiAgJ2JvdHRvbScsXG4gICdib3gtZGVjb3JhdGlvbi1icmVhaycsXG4gICdib3gtc2hhZG93JyxcbiAgJ2JveC1zaXppbmcnLFxuICAnYnJlYWstYWZ0ZXInLFxuICAnYnJlYWstYmVmb3JlJyxcbiAgJ2JyZWFrLWluc2lkZScsXG4gICdjYXB0aW9uLXNpZGUnLFxuICAnY2xlYXInLFxuICAnY2xpcCcsXG4gICdjbGlwLXBhdGgnLFxuICAnY29sb3InLFxuICAnY29sdW1uLWNvdW50JyxcbiAgJ2NvbHVtbi1maWxsJyxcbiAgJ2NvbHVtbi1nYXAnLFxuICAnY29sdW1uLXJ1bGUnLFxuICAnY29sdW1uLXJ1bGUtY29sb3InLFxuICAnY29sdW1uLXJ1bGUtc3R5bGUnLFxuICAnY29sdW1uLXJ1bGUtd2lkdGgnLFxuICAnY29sdW1uLXNwYW4nLFxuICAnY29sdW1uLXdpZHRoJyxcbiAgJ2NvbHVtbnMnLFxuICAnY29udGVudCcsXG4gICdjb3VudGVyLWluY3JlbWVudCcsXG4gICdjb3VudGVyLXJlc2V0JyxcbiAgJ2N1cnNvcicsXG4gICdkaXJlY3Rpb24nLFxuICAnZGlzcGxheScsXG4gICdlbXB0eS1jZWxscycsXG4gICdmaWx0ZXInLFxuICAnZmxleCcsXG4gICdmbGV4LWJhc2lzJyxcbiAgJ2ZsZXgtZGlyZWN0aW9uJyxcbiAgJ2ZsZXgtZmxvdycsXG4gICdmbGV4LWdyb3cnLFxuICAnZmxleC1zaHJpbmsnLFxuICAnZmxleC13cmFwJyxcbiAgJ2Zsb2F0JyxcbiAgJ2ZvbnQnLFxuICAnZm9udC1kaXNwbGF5JyxcbiAgJ2ZvbnQtZmFtaWx5JyxcbiAgJ2ZvbnQtZmVhdHVyZS1zZXR0aW5ncycsXG4gICdmb250LWtlcm5pbmcnLFxuICAnZm9udC1sYW5ndWFnZS1vdmVycmlkZScsXG4gICdmb250LXNpemUnLFxuICAnZm9udC1zaXplLWFkanVzdCcsXG4gICdmb250LXNtb290aGluZycsXG4gICdmb250LXN0cmV0Y2gnLFxuICAnZm9udC1zdHlsZScsXG4gICdmb250LXZhcmlhbnQnLFxuICAnZm9udC12YXJpYW50LWxpZ2F0dXJlcycsXG4gICdmb250LXZhcmlhdGlvbi1zZXR0aW5ncycsXG4gICdmb250LXdlaWdodCcsXG4gICdoZWlnaHQnLFxuICAnaHlwaGVucycsXG4gICdpY29uJyxcbiAgJ2ltYWdlLW9yaWVudGF0aW9uJyxcbiAgJ2ltYWdlLXJlbmRlcmluZycsXG4gICdpbWFnZS1yZXNvbHV0aW9uJyxcbiAgJ2ltZS1tb2RlJyxcbiAgJ2luaGVyaXQnLFxuICAnaW5pdGlhbCcsXG4gICdqdXN0aWZ5LWNvbnRlbnQnLFxuICAnbGVmdCcsXG4gICdsZXR0ZXItc3BhY2luZycsXG4gICdsaW5lLWhlaWdodCcsXG4gICdsaXN0LXN0eWxlJyxcbiAgJ2xpc3Qtc3R5bGUtaW1hZ2UnLFxuICAnbGlzdC1zdHlsZS1wb3NpdGlvbicsXG4gICdsaXN0LXN0eWxlLXR5cGUnLFxuICAnbWFyZ2luJyxcbiAgJ21hcmdpbi1ib3R0b20nLFxuICAnbWFyZ2luLWxlZnQnLFxuICAnbWFyZ2luLXJpZ2h0JyxcbiAgJ21hcmdpbi10b3AnLFxuICAnbWFya3MnLFxuICAnbWFzaycsXG4gICdtYXgtaGVpZ2h0JyxcbiAgJ21heC13aWR0aCcsXG4gICdtaW4taGVpZ2h0JyxcbiAgJ21pbi13aWR0aCcsXG4gICduYXYtZG93bicsXG4gICduYXYtaW5kZXgnLFxuICAnbmF2LWxlZnQnLFxuICAnbmF2LXJpZ2h0JyxcbiAgJ25hdi11cCcsXG4gICdub25lJyxcbiAgJ25vcm1hbCcsXG4gICdvYmplY3QtZml0JyxcbiAgJ29iamVjdC1wb3NpdGlvbicsXG4gICdvcGFjaXR5JyxcbiAgJ29yZGVyJyxcbiAgJ29ycGhhbnMnLFxuICAnb3V0bGluZScsXG4gICdvdXRsaW5lLWNvbG9yJyxcbiAgJ291dGxpbmUtb2Zmc2V0JyxcbiAgJ291dGxpbmUtc3R5bGUnLFxuICAnb3V0bGluZS13aWR0aCcsXG4gICdvdmVyZmxvdycsXG4gICdvdmVyZmxvdy13cmFwJyxcbiAgJ292ZXJmbG93LXgnLFxuICAnb3ZlcmZsb3cteScsXG4gICdwYWRkaW5nJyxcbiAgJ3BhZGRpbmctYm90dG9tJyxcbiAgJ3BhZGRpbmctbGVmdCcsXG4gICdwYWRkaW5nLXJpZ2h0JyxcbiAgJ3BhZGRpbmctdG9wJyxcbiAgJ3BhZ2UtYnJlYWstYWZ0ZXInLFxuICAncGFnZS1icmVhay1iZWZvcmUnLFxuICAncGFnZS1icmVhay1pbnNpZGUnLFxuICAncGVyc3BlY3RpdmUnLFxuICAncGVyc3BlY3RpdmUtb3JpZ2luJyxcbiAgJ3BvaW50ZXItZXZlbnRzJyxcbiAgJ3Bvc2l0aW9uJyxcbiAgJ3F1b3RlcycsXG4gICdyZXNpemUnLFxuICAncmlnaHQnLFxuICAnc3JjJywgLy8gQGZvbnQtZmFjZVxuICAndGFiLXNpemUnLFxuICAndGFibGUtbGF5b3V0JyxcbiAgJ3RleHQtYWxpZ24nLFxuICAndGV4dC1hbGlnbi1sYXN0JyxcbiAgJ3RleHQtZGVjb3JhdGlvbicsXG4gICd0ZXh0LWRlY29yYXRpb24tY29sb3InLFxuICAndGV4dC1kZWNvcmF0aW9uLWxpbmUnLFxuICAndGV4dC1kZWNvcmF0aW9uLXN0eWxlJyxcbiAgJ3RleHQtaW5kZW50JyxcbiAgJ3RleHQtb3ZlcmZsb3cnLFxuICAndGV4dC1yZW5kZXJpbmcnLFxuICAndGV4dC1zaGFkb3cnLFxuICAndGV4dC10cmFuc2Zvcm0nLFxuICAndGV4dC11bmRlcmxpbmUtcG9zaXRpb24nLFxuICAndG9wJyxcbiAgJ3RyYW5zZm9ybScsXG4gICd0cmFuc2Zvcm0tb3JpZ2luJyxcbiAgJ3RyYW5zZm9ybS1zdHlsZScsXG4gICd0cmFuc2l0aW9uJyxcbiAgJ3RyYW5zaXRpb24tZGVsYXknLFxuICAndHJhbnNpdGlvbi1kdXJhdGlvbicsXG4gICd0cmFuc2l0aW9uLXByb3BlcnR5JyxcbiAgJ3RyYW5zaXRpb24tdGltaW5nLWZ1bmN0aW9uJyxcbiAgJ3VuaWNvZGUtYmlkaScsXG4gICd2ZXJ0aWNhbC1hbGlnbicsXG4gICd2aXNpYmlsaXR5JyxcbiAgJ3doaXRlLXNwYWNlJyxcbiAgJ3dpZG93cycsXG4gICd3aWR0aCcsXG4gICd3b3JkLWJyZWFrJyxcbiAgJ3dvcmQtc3BhY2luZycsXG4gICd3b3JkLXdyYXAnLFxuICAnei1pbmRleCdcbiAgLy8gcmV2ZXJzZSBtYWtlcyBzdXJlIGxvbmdlciBhdHRyaWJ1dGVzIGBmb250LXdlaWdodGAgYXJlIG1hdGNoZWQgZnVsbHlcbiAgLy8gaW5zdGVhZCBvZiBnZXR0aW5nIGZhbHNlIHBvc2l0aXZlcyBvbiBzYXkgYGZvbnRgXG5dLnJldmVyc2UoKTtcblxuLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gbG9va2FoZWFkKHJlKSB7XG4gIHJldHVybiBjb25jYXQoJyg/PScsIHJlLCAnKScpO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7Li4uKFJlZ0V4cCB8IHN0cmluZykgfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBjb25jYXQoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwiXCIpO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKlxuTGFuZ3VhZ2U6IENTU1xuQ2F0ZWdvcnk6IGNvbW1vbiwgY3NzXG5XZWJzaXRlOiBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi1VUy9kb2NzL1dlYi9DU1NcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBjc3MoaGxqcykge1xuICBjb25zdCBtb2RlcyA9IE1PREVTKGhsanMpO1xuICBjb25zdCBGVU5DVElPTl9ESVNQQVRDSCA9IHtcbiAgICBjbGFzc05hbWU6IFwiYnVpbHRfaW5cIixcbiAgICBiZWdpbjogL1tcXHctXSsoPz1cXCgpL1xuICB9O1xuICBjb25zdCBWRU5ET1JfUFJFRklYID0ge1xuICAgIGJlZ2luOiAvLSh3ZWJraXR8bW96fG1zfG8pLSg/PVthLXpdKS9cbiAgfTtcbiAgY29uc3QgQVRfTU9ESUZJRVJTID0gXCJhbmQgb3Igbm90IG9ubHlcIjtcbiAgY29uc3QgQVRfUFJPUEVSVFlfUkUgPSAvQC0/XFx3W1xcd10qKC1cXHcrKSovOyAvLyBALXdlYmtpdC1rZXlmcmFtZXNcbiAgY29uc3QgSURFTlRfUkUgPSAnW2EtekEtWi1dW2EtekEtWjAtOV8tXSonO1xuICBjb25zdCBTVFJJTkdTID0gW1xuICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFXG4gIF07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQ1NTJyxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGlsbGVnYWw6IC9bPXwnXFwkXS8sXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleWZyYW1lUG9zaXRpb246IFwiZnJvbSB0b1wiXG4gICAgfSxcbiAgICBjbGFzc05hbWVBbGlhc2VzOiB7XG4gICAgICAvLyBmb3IgdmlzdWFsIGNvbnRpbnVpdHkgd2l0aCBgdGFnIHt9YCBhbmQgYmVjYXVzZSB3ZVxuICAgICAgLy8gZG9uJ3QgaGF2ZSBhIGdyZWF0IGNsYXNzIGZvciB0aGlzP1xuICAgICAga2V5ZnJhbWVQb3NpdGlvbjogXCJzZWxlY3Rvci10YWdcIlxuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBWRU5ET1JfUFJFRklYLFxuICAgICAgLy8gdG8gcmVjb2duaXplIGtleWZyYW1lIDQwJSBldGMgd2hpY2ggYXJlIG91dHNpZGUgdGhlIHNjb3BlIG9mIG91clxuICAgICAgLy8gYXR0cmlidXRlIHZhbHVlIG1vZGVcbiAgICAgIGhsanMuQ1NTX05VTUJFUl9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzZWxlY3Rvci1pZCcsXG4gICAgICAgIGJlZ2luOiAvI1tBLVphLXowLTlfLV0rLyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzZWxlY3Rvci1jbGFzcycsXG4gICAgICAgIGJlZ2luOiAnXFxcXC4nICsgSURFTlRfUkUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIG1vZGVzLkFUVFJJQlVURV9TRUxFQ1RPUl9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzZWxlY3Rvci1wc2V1ZG8nLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnOignICsgUFNFVURPX0NMQVNTRVMuam9pbignfCcpICsgJyknXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJzo6KCcgKyBQU0VVRE9fRUxFTUVOVFMuam9pbignfCcpICsgJyknXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgLy8gd2UgbWF5IGFjdHVhbGx5IG5lZWQgdGhpcyAoMTIvMjAyMClcbiAgICAgIC8vIHsgLy8gcHNldWRvLXNlbGVjdG9yIHBhcmFtc1xuICAgICAgLy8gICBiZWdpbjogL1xcKC8sXG4gICAgICAvLyAgIGVuZDogL1xcKS8sXG4gICAgICAvLyAgIGNvbnRhaW5zOiBbIGhsanMuQ1NTX05VTUJFUl9NT0RFIF1cbiAgICAgIC8vIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2F0dHJpYnV0ZScsXG4gICAgICAgIGJlZ2luOiAnXFxcXGIoJyArIEFUVFJJQlVURVMuam9pbignfCcpICsgJylcXFxcYidcbiAgICAgIH0sXG4gICAgICAvLyBhdHRyaWJ1dGUgdmFsdWVzXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnOicsXG4gICAgICAgIGVuZDogJ1s7fV0nLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIG1vZGVzLkhFWENPTE9SLFxuICAgICAgICAgIG1vZGVzLklNUE9SVEFOVCxcbiAgICAgICAgICBobGpzLkNTU19OVU1CRVJfTU9ERSxcbiAgICAgICAgICAuLi5TVFJJTkdTLFxuICAgICAgICAgIC8vIG5lZWRlZCB0byBoaWdobGlnaHQgdGhlc2UgYXMgc3RyaW5ncyBhbmQgdG8gYXZvaWQgaXNzdWVzIHdpdGhcbiAgICAgICAgICAvLyBpbGxlZ2FsIGNoYXJhY3RlcnMgdGhhdCBtaWdodCBiZSBpbnNpZGUgdXJscyB0aGF0IHdvdWxkIHRpZ2dlciB0aGVcbiAgICAgICAgICAvLyBsYW5ndWFnZXMgaWxsZWdhbCBzdGFja1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvKHVybHxkYXRhLXVyaSlcXCgvLFxuICAgICAgICAgICAgZW5kOiAvXFwpLyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMCwgLy8gZnJvbSBrZXl3b3Jkc1xuICAgICAgICAgICAga2V5d29yZHM6IHtcbiAgICAgICAgICAgICAgYnVpbHRfaW46IFwidXJsIGRhdGEtdXJpXCJcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lOiBcInN0cmluZ1wiLFxuICAgICAgICAgICAgICAgIC8vIGFueSBjaGFyYWN0ZXIgb3RoZXIgdGhhbiBgKWAgYXMgaW4gYHVybCgpYCB3aWxsIGJlIHRoZSBzdGFydFxuICAgICAgICAgICAgICAgIC8vIG9mIGEgc3RyaW5nLCB3aGljaCBlbmRzIHdpdGggYClgIChmcm9tIHRoZSBwYXJlbnQgbW9kZSlcbiAgICAgICAgICAgICAgICBiZWdpbjogL1teKV0vLFxuICAgICAgICAgICAgICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH0sXG4gICAgICAgICAgRlVOQ1RJT05fRElTUEFUQ0hcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IGxvb2thaGVhZCgvQC8pLFxuICAgICAgICBlbmQ6ICdbeztdJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBpbGxlZ2FsOiAvOi8sIC8vIGJyZWFrIG9uIExlc3MgdmFyaWFibGVzIEB2YXI6IC4uLlxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgICAgICAgICAgYmVnaW46IEFUX1BST1BFUlRZX1JFXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL1xccy8sXG4gICAgICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgICBrZXl3b3Jkczoge1xuICAgICAgICAgICAgICAkcGF0dGVybjogL1thLXotXSsvLFxuICAgICAgICAgICAgICBrZXl3b3JkOiBBVF9NT0RJRklFUlMsXG4gICAgICAgICAgICAgIGF0dHJpYnV0ZTogTUVESUFfRkVBVFVSRVMuam9pbihcIiBcIilcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgYmVnaW46IC9bYS16LV0rKD89OikvLFxuICAgICAgICAgICAgICAgIGNsYXNzTmFtZTogXCJhdHRyaWJ1dGVcIlxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICAuLi5TVFJJTkdTLFxuICAgICAgICAgICAgICBobGpzLkNTU19OVU1CRVJfTU9ERVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc2VsZWN0b3ItdGFnJyxcbiAgICAgICAgYmVnaW46ICdcXFxcYignICsgVEFHUy5qb2luKCd8JykgKyAnKVxcXFxiJ1xuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBjc3M7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=