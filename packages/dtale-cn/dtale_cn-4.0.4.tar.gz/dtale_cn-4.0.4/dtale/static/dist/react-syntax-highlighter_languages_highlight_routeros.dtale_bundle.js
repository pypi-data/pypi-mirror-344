(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_routeros"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/routeros.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/routeros.js ***!
  \***************************************************************************************************/
/***/ ((module) => {

/*
Language: Microtik RouterOS script
Author: Ivan Dementev <ivan_div@mail.ru>
Description: Scripting host provides a way to automate some router maintenance tasks by means of executing user-defined scripts bounded to some event occurrence
Website: https://wiki.mikrotik.com/wiki/Manual:Scripting
*/

// Colors from RouterOS terminal:
//   green        - #0E9A00
//   teal         - #0C9A9A
//   purple       - #99069A
//   light-brown  - #9A9900

function routeros(hljs) {
  const STATEMENTS = 'foreach do while for if from to step else on-error and or not in';

  // Global commands: Every global command should start with ":" token, otherwise it will be treated as variable.
  const GLOBAL_COMMANDS = 'global local beep delay put len typeof pick log time set find environment terminal error execute parse resolve toarray tobool toid toip toip6 tonum tostr totime';

  // Common commands: Following commands available from most sub-menus:
  const COMMON_COMMANDS = 'add remove enable disable set get print export edit find run debug error info warning';

  const LITERALS = 'true false yes no nothing nil null';

  const OBJECTS = 'traffic-flow traffic-generator firewall scheduler aaa accounting address-list address align area bandwidth-server bfd bgp bridge client clock community config connection console customer default dhcp-client dhcp-server discovery dns e-mail ethernet filter firmware gps graphing group hardware health hotspot identity igmp-proxy incoming instance interface ip ipsec ipv6 irq l2tp-server lcd ldp logging mac-server mac-winbox mangle manual mirror mme mpls nat nd neighbor network note ntp ospf ospf-v3 ovpn-server page peer pim ping policy pool port ppp pppoe-client pptp-server prefix profile proposal proxy queue radius resource rip ripng route routing screen script security-profiles server service service-port settings shares smb sms sniffer snmp snooper socks sstp-server system tool tracking type upgrade upnp user-manager users user vlan secret vrrp watchdog web-access wireless pptp pppoe lan wan layer7-protocol lease simple raw';

  const VAR = {
    className: 'variable',
    variants: [
      {
        begin: /\$[\w\d#@][\w\d_]*/
      },
      {
        begin: /\$\{(.*?)\}/
      }
    ]
  };

  const QUOTE_STRING = {
    className: 'string',
    begin: /"/,
    end: /"/,
    contains: [
      hljs.BACKSLASH_ESCAPE,
      VAR,
      {
        className: 'variable',
        begin: /\$\(/,
        end: /\)/,
        contains: [ hljs.BACKSLASH_ESCAPE ]
      }
    ]
  };

  const APOS_STRING = {
    className: 'string',
    begin: /'/,
    end: /'/
  };

  return {
    name: 'Microtik RouterOS script',
    aliases: [
      'mikrotik'
    ],
    case_insensitive: true,
    keywords: {
      $pattern: /:?[\w-]+/,
      literal: LITERALS,
      keyword: STATEMENTS + ' :' + STATEMENTS.split(' ').join(' :') + ' :' + GLOBAL_COMMANDS.split(' ').join(' :')
    },
    contains: [
      { // illegal syntax
        variants: [
          { // -- comment
            begin: /\/\*/,
            end: /\*\//
          },
          { // Stan comment
            begin: /\/\//,
            end: /$/
          },
          { // HTML tags
            begin: /<\//,
            end: />/
          }
        ],
        illegal: /./
      },
      hljs.COMMENT('^#', '$'),
      QUOTE_STRING,
      APOS_STRING,
      VAR,
      // attribute=value
      {
        // > is to avoid matches with => in other grammars
        begin: /[\w-]+=([^\s{}[\]()>]+)/,
        relevance: 0,
        returnBegin: true,
        contains: [
          {
            className: 'attribute',
            begin: /[^=]+/
          },
          {
            begin: /=/,
            endsWithParent: true,
            relevance: 0,
            contains: [
              QUOTE_STRING,
              APOS_STRING,
              VAR,
              {
                className: 'literal',
                begin: '\\b(' + LITERALS.split(' ').join('|') + ')\\b'
              },
              {
                // Do not format unclassified values. Needed to exclude highlighting of values as built_in.
                begin: /("[^"]*"|[^\s{}[\]]+)/
              }
              /*
              {
                // IPv4 addresses and subnets
                className: 'number',
                variants: [
                  {begin: IPADDR_wBITMASK+'(,'+IPADDR_wBITMASK+')*'}, //192.168.0.0/24,1.2.3.0/24
                  {begin: IPADDR+'-'+IPADDR},       // 192.168.0.1-192.168.0.3
                  {begin: IPADDR+'(,'+IPADDR+')*'}, // 192.168.0.1,192.168.0.34,192.168.24.1,192.168.0.1
                ]
              },
              {
                // MAC addresses and DHCP Client IDs
                className: 'number',
                begin: /\b(1:)?([0-9A-Fa-f]{1,2}[:-]){5}([0-9A-Fa-f]){1,2}\b/,
              },
              */
            ]
          }
        ]
      },
      {
        // HEX values
        className: 'number',
        begin: /\*[0-9a-fA-F]+/
      },
      {
        begin: '\\b(' + COMMON_COMMANDS.split(' ').join('|') + ')([\\s[(\\]|])',
        returnBegin: true,
        contains: [
          {
            className: 'builtin-name', // 'function',
            begin: /\w+/
          }
        ]
      },
      {
        className: 'built_in',
        variants: [
          {
            begin: '(\\.\\./|/|\\s)((' + OBJECTS.split(' ').join('|') + ');?\\s)+'
          },
          {
            begin: /\.\./,
            relevance: 0
          }
        ]
      }
    ]
  };
}

module.exports = routeros;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcm91dGVyb3MuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBLG9CQUFvQixPQUFPO0FBQzNCO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBLFFBQVE7QUFDUjtBQUNBLFlBQVk7QUFDWjtBQUNBO0FBQ0EsV0FBVztBQUNYLFlBQVk7QUFDWjtBQUNBO0FBQ0EsV0FBVztBQUNYLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsOEJBQThCO0FBQzlCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQSx1Q0FBdUM7QUFDdkM7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsbUJBQW1CLGlEQUFpRDtBQUNwRSxtQkFBbUIseUJBQXlCO0FBQzVDLG1CQUFtQiwrQkFBK0I7QUFDbEQ7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0EsNENBQTRDLElBQUksTUFBTSxFQUFFLGNBQWMsSUFBSTtBQUMxRSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsMkVBQTJFO0FBQzNFLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3JvdXRlcm9zLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTWljcm90aWsgUm91dGVyT1Mgc2NyaXB0XG5BdXRob3I6IEl2YW4gRGVtZW50ZXYgPGl2YW5fZGl2QG1haWwucnU+XG5EZXNjcmlwdGlvbjogU2NyaXB0aW5nIGhvc3QgcHJvdmlkZXMgYSB3YXkgdG8gYXV0b21hdGUgc29tZSByb3V0ZXIgbWFpbnRlbmFuY2UgdGFza3MgYnkgbWVhbnMgb2YgZXhlY3V0aW5nIHVzZXItZGVmaW5lZCBzY3JpcHRzIGJvdW5kZWQgdG8gc29tZSBldmVudCBvY2N1cnJlbmNlXG5XZWJzaXRlOiBodHRwczovL3dpa2kubWlrcm90aWsuY29tL3dpa2kvTWFudWFsOlNjcmlwdGluZ1xuKi9cblxuLy8gQ29sb3JzIGZyb20gUm91dGVyT1MgdGVybWluYWw6XG4vLyAgIGdyZWVuICAgICAgICAtICMwRTlBMDBcbi8vICAgdGVhbCAgICAgICAgIC0gIzBDOUE5QVxuLy8gICBwdXJwbGUgICAgICAgLSAjOTkwNjlBXG4vLyAgIGxpZ2h0LWJyb3duICAtICM5QTk5MDBcblxuZnVuY3Rpb24gcm91dGVyb3MoaGxqcykge1xuICBjb25zdCBTVEFURU1FTlRTID0gJ2ZvcmVhY2ggZG8gd2hpbGUgZm9yIGlmIGZyb20gdG8gc3RlcCBlbHNlIG9uLWVycm9yIGFuZCBvciBub3QgaW4nO1xuXG4gIC8vIEdsb2JhbCBjb21tYW5kczogRXZlcnkgZ2xvYmFsIGNvbW1hbmQgc2hvdWxkIHN0YXJ0IHdpdGggXCI6XCIgdG9rZW4sIG90aGVyd2lzZSBpdCB3aWxsIGJlIHRyZWF0ZWQgYXMgdmFyaWFibGUuXG4gIGNvbnN0IEdMT0JBTF9DT01NQU5EUyA9ICdnbG9iYWwgbG9jYWwgYmVlcCBkZWxheSBwdXQgbGVuIHR5cGVvZiBwaWNrIGxvZyB0aW1lIHNldCBmaW5kIGVudmlyb25tZW50IHRlcm1pbmFsIGVycm9yIGV4ZWN1dGUgcGFyc2UgcmVzb2x2ZSB0b2FycmF5IHRvYm9vbCB0b2lkIHRvaXAgdG9pcDYgdG9udW0gdG9zdHIgdG90aW1lJztcblxuICAvLyBDb21tb24gY29tbWFuZHM6IEZvbGxvd2luZyBjb21tYW5kcyBhdmFpbGFibGUgZnJvbSBtb3N0IHN1Yi1tZW51czpcbiAgY29uc3QgQ09NTU9OX0NPTU1BTkRTID0gJ2FkZCByZW1vdmUgZW5hYmxlIGRpc2FibGUgc2V0IGdldCBwcmludCBleHBvcnQgZWRpdCBmaW5kIHJ1biBkZWJ1ZyBlcnJvciBpbmZvIHdhcm5pbmcnO1xuXG4gIGNvbnN0IExJVEVSQUxTID0gJ3RydWUgZmFsc2UgeWVzIG5vIG5vdGhpbmcgbmlsIG51bGwnO1xuXG4gIGNvbnN0IE9CSkVDVFMgPSAndHJhZmZpYy1mbG93IHRyYWZmaWMtZ2VuZXJhdG9yIGZpcmV3YWxsIHNjaGVkdWxlciBhYWEgYWNjb3VudGluZyBhZGRyZXNzLWxpc3QgYWRkcmVzcyBhbGlnbiBhcmVhIGJhbmR3aWR0aC1zZXJ2ZXIgYmZkIGJncCBicmlkZ2UgY2xpZW50IGNsb2NrIGNvbW11bml0eSBjb25maWcgY29ubmVjdGlvbiBjb25zb2xlIGN1c3RvbWVyIGRlZmF1bHQgZGhjcC1jbGllbnQgZGhjcC1zZXJ2ZXIgZGlzY292ZXJ5IGRucyBlLW1haWwgZXRoZXJuZXQgZmlsdGVyIGZpcm13YXJlIGdwcyBncmFwaGluZyBncm91cCBoYXJkd2FyZSBoZWFsdGggaG90c3BvdCBpZGVudGl0eSBpZ21wLXByb3h5IGluY29taW5nIGluc3RhbmNlIGludGVyZmFjZSBpcCBpcHNlYyBpcHY2IGlycSBsMnRwLXNlcnZlciBsY2QgbGRwIGxvZ2dpbmcgbWFjLXNlcnZlciBtYWMtd2luYm94IG1hbmdsZSBtYW51YWwgbWlycm9yIG1tZSBtcGxzIG5hdCBuZCBuZWlnaGJvciBuZXR3b3JrIG5vdGUgbnRwIG9zcGYgb3NwZi12MyBvdnBuLXNlcnZlciBwYWdlIHBlZXIgcGltIHBpbmcgcG9saWN5IHBvb2wgcG9ydCBwcHAgcHBwb2UtY2xpZW50IHBwdHAtc2VydmVyIHByZWZpeCBwcm9maWxlIHByb3Bvc2FsIHByb3h5IHF1ZXVlIHJhZGl1cyByZXNvdXJjZSByaXAgcmlwbmcgcm91dGUgcm91dGluZyBzY3JlZW4gc2NyaXB0IHNlY3VyaXR5LXByb2ZpbGVzIHNlcnZlciBzZXJ2aWNlIHNlcnZpY2UtcG9ydCBzZXR0aW5ncyBzaGFyZXMgc21iIHNtcyBzbmlmZmVyIHNubXAgc25vb3BlciBzb2NrcyBzc3RwLXNlcnZlciBzeXN0ZW0gdG9vbCB0cmFja2luZyB0eXBlIHVwZ3JhZGUgdXBucCB1c2VyLW1hbmFnZXIgdXNlcnMgdXNlciB2bGFuIHNlY3JldCB2cnJwIHdhdGNoZG9nIHdlYi1hY2Nlc3Mgd2lyZWxlc3MgcHB0cCBwcHBvZSBsYW4gd2FuIGxheWVyNy1wcm90b2NvbCBsZWFzZSBzaW1wbGUgcmF3JztcblxuICBjb25zdCBWQVIgPSB7XG4gICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwkW1xcd1xcZCNAXVtcXHdcXGRfXSovXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcJFxceyguKj8pXFx9L1xuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBRVU9URV9TVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogL1wiLyxcbiAgICBlbmQ6IC9cIi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgIFZBUixcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgICAgICBiZWdpbjogL1xcJFxcKC8sXG4gICAgICAgIGVuZDogL1xcKS8sXG4gICAgICAgIGNvbnRhaW5zOiBbIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSBdXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IEFQT1NfU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46IC8nLyxcbiAgICBlbmQ6IC8nL1xuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ01pY3JvdGlrIFJvdXRlck9TIHNjcmlwdCcsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ21pa3JvdGlrJ1xuICAgIF0sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJHBhdHRlcm46IC86P1tcXHctXSsvLFxuICAgICAgbGl0ZXJhbDogTElURVJBTFMsXG4gICAgICBrZXl3b3JkOiBTVEFURU1FTlRTICsgJyA6JyArIFNUQVRFTUVOVFMuc3BsaXQoJyAnKS5qb2luKCcgOicpICsgJyA6JyArIEdMT0JBTF9DT01NQU5EUy5zcGxpdCgnICcpLmpvaW4oJyA6JylcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7IC8vIGlsbGVnYWwgc3ludGF4XG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAgeyAvLyAtLSBjb21tZW50XG4gICAgICAgICAgICBiZWdpbjogL1xcL1xcKi8sXG4gICAgICAgICAgICBlbmQ6IC9cXCpcXC8vXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7IC8vIFN0YW4gY29tbWVudFxuICAgICAgICAgICAgYmVnaW46IC9cXC9cXC8vLFxuICAgICAgICAgICAgZW5kOiAvJC9cbiAgICAgICAgICB9LFxuICAgICAgICAgIHsgLy8gSFRNTCB0YWdzXG4gICAgICAgICAgICBiZWdpbjogLzxcXC8vLFxuICAgICAgICAgICAgZW5kOiAvPi9cbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICAgIGlsbGVnYWw6IC8uL1xuICAgICAgfSxcbiAgICAgIGhsanMuQ09NTUVOVCgnXiMnLCAnJCcpLFxuICAgICAgUVVPVEVfU1RSSU5HLFxuICAgICAgQVBPU19TVFJJTkcsXG4gICAgICBWQVIsXG4gICAgICAvLyBhdHRyaWJ1dGU9dmFsdWVcbiAgICAgIHtcbiAgICAgICAgLy8gPiBpcyB0byBhdm9pZCBtYXRjaGVzIHdpdGggPT4gaW4gb3RoZXIgZ3JhbW1hcnNcbiAgICAgICAgYmVnaW46IC9bXFx3LV0rPShbXlxcc3t9W1xcXSgpPl0rKS8sXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnYXR0cmlidXRlJyxcbiAgICAgICAgICAgIGJlZ2luOiAvW149XSsvXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogLz0vLFxuICAgICAgICAgICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICBRVU9URV9TVFJJTkcsXG4gICAgICAgICAgICAgIEFQT1NfU1RSSU5HLFxuICAgICAgICAgICAgICBWQVIsXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBjbGFzc05hbWU6ICdsaXRlcmFsJyxcbiAgICAgICAgICAgICAgICBiZWdpbjogJ1xcXFxiKCcgKyBMSVRFUkFMUy5zcGxpdCgnICcpLmpvaW4oJ3wnKSArICcpXFxcXGInXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAvLyBEbyBub3QgZm9ybWF0IHVuY2xhc3NpZmllZCB2YWx1ZXMuIE5lZWRlZCB0byBleGNsdWRlIGhpZ2hsaWdodGluZyBvZiB2YWx1ZXMgYXMgYnVpbHRfaW4uXG4gICAgICAgICAgICAgICAgYmVnaW46IC8oXCJbXlwiXSpcInxbXlxcc3t9W1xcXV0rKS9cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAvKlxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgLy8gSVB2NCBhZGRyZXNzZXMgYW5kIHN1Ym5ldHNcbiAgICAgICAgICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICAgICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAgICAgICAgICB7YmVnaW46IElQQUREUl93QklUTUFTSysnKCwnK0lQQUREUl93QklUTUFTSysnKSonfSwgLy8xOTIuMTY4LjAuMC8yNCwxLjIuMy4wLzI0XG4gICAgICAgICAgICAgICAgICB7YmVnaW46IElQQUREUisnLScrSVBBRERSfSwgICAgICAgLy8gMTkyLjE2OC4wLjEtMTkyLjE2OC4wLjNcbiAgICAgICAgICAgICAgICAgIHtiZWdpbjogSVBBRERSKycoLCcrSVBBRERSKycpKid9LCAvLyAxOTIuMTY4LjAuMSwxOTIuMTY4LjAuMzQsMTkyLjE2OC4yNC4xLDE5Mi4xNjguMC4xXG4gICAgICAgICAgICAgICAgXVxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgLy8gTUFDIGFkZHJlc3NlcyBhbmQgREhDUCBDbGllbnQgSURzXG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgICAgICAgICBiZWdpbjogL1xcYigxOik/KFswLTlBLUZhLWZdezEsMn1bOi1dKXs1fShbMC05QS1GYS1mXSl7MSwyfVxcYi8sXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICovXG4gICAgICAgICAgICBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBIRVggdmFsdWVzXG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIGJlZ2luOiAvXFwqWzAtOWEtZkEtRl0rL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXFxcYignICsgQ09NTU9OX0NPTU1BTkRTLnNwbGl0KCcgJykuam9pbignfCcpICsgJykoW1xcXFxzWyhcXFxcXXxdKScsXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ2J1aWx0aW4tbmFtZScsIC8vICdmdW5jdGlvbicsXG4gICAgICAgICAgICBiZWdpbjogL1xcdysvXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdidWlsdF9pbicsXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICcoXFxcXC5cXFxcLi98L3xcXFxccykoKCcgKyBPQkpFQ1RTLnNwbGl0KCcgJykuam9pbignfCcpICsgJyk7P1xcXFxzKSsnXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL1xcLlxcLi8sXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcm91dGVyb3M7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=