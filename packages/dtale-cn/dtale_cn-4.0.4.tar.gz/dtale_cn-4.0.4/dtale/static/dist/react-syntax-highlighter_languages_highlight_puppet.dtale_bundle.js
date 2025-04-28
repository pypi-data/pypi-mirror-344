(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_puppet"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/puppet.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/puppet.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Puppet
Author: Jose Molina Colmenero <gaudy41@gmail.com>
Website: https://puppet.com/docs
Category: config
*/

function puppet(hljs) {
  const PUPPET_KEYWORDS = {
    keyword:
    /* language keywords */
      'and case default else elsif false if in import enherits node or true undef unless main settings $string ',
    literal:
    /* metaparameters */
      'alias audit before loglevel noop require subscribe tag ' +
      /* normal attributes */
      'owner ensure group mode name|0 changes context force incl lens load_path onlyif provider returns root show_diff type_check ' +
      'en_address ip_address realname command environment hour monute month monthday special target weekday ' +
      'creates cwd ogoutput refresh refreshonly tries try_sleep umask backup checksum content ctime force ignore ' +
      'links mtime purge recurse recurselimit replace selinux_ignore_defaults selrange selrole seltype seluser source ' +
      'souirce_permissions sourceselect validate_cmd validate_replacement allowdupe attribute_membership auth_membership forcelocal gid ' +
      'ia_load_module members system host_aliases ip allowed_trunk_vlans description device_url duplex encapsulation etherchannel ' +
      'native_vlan speed principals allow_root auth_class auth_type authenticate_user k_of_n mechanisms rule session_owner shared options ' +
      'device fstype enable hasrestart directory present absent link atboot blockdevice device dump pass remounts poller_tag use ' +
      'message withpath adminfile allow_virtual allowcdrom category configfiles flavor install_options instance package_settings platform ' +
      'responsefile status uninstall_options vendor unless_system_user unless_uid binary control flags hasstatus manifest pattern restart running ' +
      'start stop allowdupe auths expiry gid groups home iterations key_membership keys managehome membership password password_max_age ' +
      'password_min_age profile_membership profiles project purge_ssh_keys role_membership roles salt shell uid baseurl cost descr enabled ' +
      'enablegroups exclude failovermethod gpgcheck gpgkey http_caching include includepkgs keepalive metadata_expire metalink mirrorlist ' +
      'priority protect proxy proxy_password proxy_username repo_gpgcheck s3_enabled skip_if_unavailable sslcacert sslclientcert sslclientkey ' +
      'sslverify mounted',
    built_in:
    /* core facts */
      'architecture augeasversion blockdevices boardmanufacturer boardproductname boardserialnumber cfkey dhcp_servers ' +
      'domain ec2_ ec2_userdata facterversion filesystems ldom fqdn gid hardwareisa hardwaremodel hostname id|0 interfaces ' +
      'ipaddress ipaddress_ ipaddress6 ipaddress6_ iphostnumber is_virtual kernel kernelmajversion kernelrelease kernelversion ' +
      'kernelrelease kernelversion lsbdistcodename lsbdistdescription lsbdistid lsbdistrelease lsbmajdistrelease lsbminordistrelease ' +
      'lsbrelease macaddress macaddress_ macosx_buildversion macosx_productname macosx_productversion macosx_productverson_major ' +
      'macosx_productversion_minor manufacturer memoryfree memorysize netmask metmask_ network_ operatingsystem operatingsystemmajrelease ' +
      'operatingsystemrelease osfamily partitions path physicalprocessorcount processor processorcount productname ps puppetversion ' +
      'rubysitedir rubyversion selinux selinux_config_mode selinux_config_policy selinux_current_mode selinux_current_mode selinux_enforced ' +
      'selinux_policyversion serialnumber sp_ sshdsakey sshecdsakey sshrsakey swapencrypted swapfree swapsize timezone type uniqueid uptime ' +
      'uptime_days uptime_hours uptime_seconds uuid virtual vlans xendomains zfs_version zonenae zones zpool_version'
  };

  const COMMENT = hljs.COMMENT('#', '$');

  const IDENT_RE = '([A-Za-z_]|::)(\\w|::)*';

  const TITLE = hljs.inherit(hljs.TITLE_MODE, {
    begin: IDENT_RE
  });

  const VARIABLE = {
    className: 'variable',
    begin: '\\$' + IDENT_RE
  };

  const STRING = {
    className: 'string',
    contains: [
      hljs.BACKSLASH_ESCAPE,
      VARIABLE
    ],
    variants: [
      {
        begin: /'/,
        end: /'/
      },
      {
        begin: /"/,
        end: /"/
      }
    ]
  };

  return {
    name: 'Puppet',
    aliases: [ 'pp' ],
    contains: [
      COMMENT,
      VARIABLE,
      STRING,
      {
        beginKeywords: 'class',
        end: '\\{|;',
        illegal: /=/,
        contains: [
          TITLE,
          COMMENT
        ]
      },
      {
        beginKeywords: 'define',
        end: /\{/,
        contains: [
          {
            className: 'section',
            begin: hljs.IDENT_RE,
            endsParent: true
          }
        ]
      },
      {
        begin: hljs.IDENT_RE + '\\s+\\{',
        returnBegin: true,
        end: /\S/,
        contains: [
          {
            className: 'keyword',
            begin: hljs.IDENT_RE
          },
          {
            begin: /\{/,
            end: /\}/,
            keywords: PUPPET_KEYWORDS,
            relevance: 0,
            contains: [
              STRING,
              COMMENT,
              {
                begin: '[a-zA-Z_]+\\s*=>',
                returnBegin: true,
                end: '=>',
                contains: [
                  {
                    className: 'attr',
                    begin: hljs.IDENT_RE
                  }
                ]
              },
              {
                className: 'number',
                begin: '(\\b0[0-7_]+)|(\\b0x[0-9a-fA-F_]+)|(\\b[1-9][0-9_]*(\\.[0-9_]+)?)|[0_]\\b',
                relevance: 0
              },
              VARIABLE
            ]
          }
        ],
        relevance: 0
      }
    ]
  };
}

module.exports = puppet;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcHVwcGV0LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0EsR0FBRzs7QUFFSDtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCLEVBQUU7QUFDbkI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0EsdUNBQXVDO0FBQ3ZDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBLHNCQUFzQjtBQUN0QixvQkFBb0I7QUFDcEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvcHVwcGV0LmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogUHVwcGV0XG5BdXRob3I6IEpvc2UgTW9saW5hIENvbG1lbmVybyA8Z2F1ZHk0MUBnbWFpbC5jb20+XG5XZWJzaXRlOiBodHRwczovL3B1cHBldC5jb20vZG9jc1xuQ2F0ZWdvcnk6IGNvbmZpZ1xuKi9cblxuZnVuY3Rpb24gcHVwcGV0KGhsanMpIHtcbiAgY29uc3QgUFVQUEVUX0tFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6XG4gICAgLyogbGFuZ3VhZ2Uga2V5d29yZHMgKi9cbiAgICAgICdhbmQgY2FzZSBkZWZhdWx0IGVsc2UgZWxzaWYgZmFsc2UgaWYgaW4gaW1wb3J0IGVuaGVyaXRzIG5vZGUgb3IgdHJ1ZSB1bmRlZiB1bmxlc3MgbWFpbiBzZXR0aW5ncyAkc3RyaW5nICcsXG4gICAgbGl0ZXJhbDpcbiAgICAvKiBtZXRhcGFyYW1ldGVycyAqL1xuICAgICAgJ2FsaWFzIGF1ZGl0IGJlZm9yZSBsb2dsZXZlbCBub29wIHJlcXVpcmUgc3Vic2NyaWJlIHRhZyAnICtcbiAgICAgIC8qIG5vcm1hbCBhdHRyaWJ1dGVzICovXG4gICAgICAnb3duZXIgZW5zdXJlIGdyb3VwIG1vZGUgbmFtZXwwIGNoYW5nZXMgY29udGV4dCBmb3JjZSBpbmNsIGxlbnMgbG9hZF9wYXRoIG9ubHlpZiBwcm92aWRlciByZXR1cm5zIHJvb3Qgc2hvd19kaWZmIHR5cGVfY2hlY2sgJyArXG4gICAgICAnZW5fYWRkcmVzcyBpcF9hZGRyZXNzIHJlYWxuYW1lIGNvbW1hbmQgZW52aXJvbm1lbnQgaG91ciBtb251dGUgbW9udGggbW9udGhkYXkgc3BlY2lhbCB0YXJnZXQgd2Vla2RheSAnICtcbiAgICAgICdjcmVhdGVzIGN3ZCBvZ291dHB1dCByZWZyZXNoIHJlZnJlc2hvbmx5IHRyaWVzIHRyeV9zbGVlcCB1bWFzayBiYWNrdXAgY2hlY2tzdW0gY29udGVudCBjdGltZSBmb3JjZSBpZ25vcmUgJyArXG4gICAgICAnbGlua3MgbXRpbWUgcHVyZ2UgcmVjdXJzZSByZWN1cnNlbGltaXQgcmVwbGFjZSBzZWxpbnV4X2lnbm9yZV9kZWZhdWx0cyBzZWxyYW5nZSBzZWxyb2xlIHNlbHR5cGUgc2VsdXNlciBzb3VyY2UgJyArXG4gICAgICAnc291aXJjZV9wZXJtaXNzaW9ucyBzb3VyY2VzZWxlY3QgdmFsaWRhdGVfY21kIHZhbGlkYXRlX3JlcGxhY2VtZW50IGFsbG93ZHVwZSBhdHRyaWJ1dGVfbWVtYmVyc2hpcCBhdXRoX21lbWJlcnNoaXAgZm9yY2Vsb2NhbCBnaWQgJyArXG4gICAgICAnaWFfbG9hZF9tb2R1bGUgbWVtYmVycyBzeXN0ZW0gaG9zdF9hbGlhc2VzIGlwIGFsbG93ZWRfdHJ1bmtfdmxhbnMgZGVzY3JpcHRpb24gZGV2aWNlX3VybCBkdXBsZXggZW5jYXBzdWxhdGlvbiBldGhlcmNoYW5uZWwgJyArXG4gICAgICAnbmF0aXZlX3ZsYW4gc3BlZWQgcHJpbmNpcGFscyBhbGxvd19yb290IGF1dGhfY2xhc3MgYXV0aF90eXBlIGF1dGhlbnRpY2F0ZV91c2VyIGtfb2ZfbiBtZWNoYW5pc21zIHJ1bGUgc2Vzc2lvbl9vd25lciBzaGFyZWQgb3B0aW9ucyAnICtcbiAgICAgICdkZXZpY2UgZnN0eXBlIGVuYWJsZSBoYXNyZXN0YXJ0IGRpcmVjdG9yeSBwcmVzZW50IGFic2VudCBsaW5rIGF0Ym9vdCBibG9ja2RldmljZSBkZXZpY2UgZHVtcCBwYXNzIHJlbW91bnRzIHBvbGxlcl90YWcgdXNlICcgK1xuICAgICAgJ21lc3NhZ2Ugd2l0aHBhdGggYWRtaW5maWxlIGFsbG93X3ZpcnR1YWwgYWxsb3djZHJvbSBjYXRlZ29yeSBjb25maWdmaWxlcyBmbGF2b3IgaW5zdGFsbF9vcHRpb25zIGluc3RhbmNlIHBhY2thZ2Vfc2V0dGluZ3MgcGxhdGZvcm0gJyArXG4gICAgICAncmVzcG9uc2VmaWxlIHN0YXR1cyB1bmluc3RhbGxfb3B0aW9ucyB2ZW5kb3IgdW5sZXNzX3N5c3RlbV91c2VyIHVubGVzc191aWQgYmluYXJ5IGNvbnRyb2wgZmxhZ3MgaGFzc3RhdHVzIG1hbmlmZXN0IHBhdHRlcm4gcmVzdGFydCBydW5uaW5nICcgK1xuICAgICAgJ3N0YXJ0IHN0b3AgYWxsb3dkdXBlIGF1dGhzIGV4cGlyeSBnaWQgZ3JvdXBzIGhvbWUgaXRlcmF0aW9ucyBrZXlfbWVtYmVyc2hpcCBrZXlzIG1hbmFnZWhvbWUgbWVtYmVyc2hpcCBwYXNzd29yZCBwYXNzd29yZF9tYXhfYWdlICcgK1xuICAgICAgJ3Bhc3N3b3JkX21pbl9hZ2UgcHJvZmlsZV9tZW1iZXJzaGlwIHByb2ZpbGVzIHByb2plY3QgcHVyZ2Vfc3NoX2tleXMgcm9sZV9tZW1iZXJzaGlwIHJvbGVzIHNhbHQgc2hlbGwgdWlkIGJhc2V1cmwgY29zdCBkZXNjciBlbmFibGVkICcgK1xuICAgICAgJ2VuYWJsZWdyb3VwcyBleGNsdWRlIGZhaWxvdmVybWV0aG9kIGdwZ2NoZWNrIGdwZ2tleSBodHRwX2NhY2hpbmcgaW5jbHVkZSBpbmNsdWRlcGtncyBrZWVwYWxpdmUgbWV0YWRhdGFfZXhwaXJlIG1ldGFsaW5rIG1pcnJvcmxpc3QgJyArXG4gICAgICAncHJpb3JpdHkgcHJvdGVjdCBwcm94eSBwcm94eV9wYXNzd29yZCBwcm94eV91c2VybmFtZSByZXBvX2dwZ2NoZWNrIHMzX2VuYWJsZWQgc2tpcF9pZl91bmF2YWlsYWJsZSBzc2xjYWNlcnQgc3NsY2xpZW50Y2VydCBzc2xjbGllbnRrZXkgJyArXG4gICAgICAnc3NsdmVyaWZ5IG1vdW50ZWQnLFxuICAgIGJ1aWx0X2luOlxuICAgIC8qIGNvcmUgZmFjdHMgKi9cbiAgICAgICdhcmNoaXRlY3R1cmUgYXVnZWFzdmVyc2lvbiBibG9ja2RldmljZXMgYm9hcmRtYW51ZmFjdHVyZXIgYm9hcmRwcm9kdWN0bmFtZSBib2FyZHNlcmlhbG51bWJlciBjZmtleSBkaGNwX3NlcnZlcnMgJyArXG4gICAgICAnZG9tYWluIGVjMl8gZWMyX3VzZXJkYXRhIGZhY3RlcnZlcnNpb24gZmlsZXN5c3RlbXMgbGRvbSBmcWRuIGdpZCBoYXJkd2FyZWlzYSBoYXJkd2FyZW1vZGVsIGhvc3RuYW1lIGlkfDAgaW50ZXJmYWNlcyAnICtcbiAgICAgICdpcGFkZHJlc3MgaXBhZGRyZXNzXyBpcGFkZHJlc3M2IGlwYWRkcmVzczZfIGlwaG9zdG51bWJlciBpc192aXJ0dWFsIGtlcm5lbCBrZXJuZWxtYWp2ZXJzaW9uIGtlcm5lbHJlbGVhc2Uga2VybmVsdmVyc2lvbiAnICtcbiAgICAgICdrZXJuZWxyZWxlYXNlIGtlcm5lbHZlcnNpb24gbHNiZGlzdGNvZGVuYW1lIGxzYmRpc3RkZXNjcmlwdGlvbiBsc2JkaXN0aWQgbHNiZGlzdHJlbGVhc2UgbHNibWFqZGlzdHJlbGVhc2UgbHNibWlub3JkaXN0cmVsZWFzZSAnICtcbiAgICAgICdsc2JyZWxlYXNlIG1hY2FkZHJlc3MgbWFjYWRkcmVzc18gbWFjb3N4X2J1aWxkdmVyc2lvbiBtYWNvc3hfcHJvZHVjdG5hbWUgbWFjb3N4X3Byb2R1Y3R2ZXJzaW9uIG1hY29zeF9wcm9kdWN0dmVyc29uX21ham9yICcgK1xuICAgICAgJ21hY29zeF9wcm9kdWN0dmVyc2lvbl9taW5vciBtYW51ZmFjdHVyZXIgbWVtb3J5ZnJlZSBtZW1vcnlzaXplIG5ldG1hc2sgbWV0bWFza18gbmV0d29ya18gb3BlcmF0aW5nc3lzdGVtIG9wZXJhdGluZ3N5c3RlbW1hanJlbGVhc2UgJyArXG4gICAgICAnb3BlcmF0aW5nc3lzdGVtcmVsZWFzZSBvc2ZhbWlseSBwYXJ0aXRpb25zIHBhdGggcGh5c2ljYWxwcm9jZXNzb3Jjb3VudCBwcm9jZXNzb3IgcHJvY2Vzc29yY291bnQgcHJvZHVjdG5hbWUgcHMgcHVwcGV0dmVyc2lvbiAnICtcbiAgICAgICdydWJ5c2l0ZWRpciBydWJ5dmVyc2lvbiBzZWxpbnV4IHNlbGludXhfY29uZmlnX21vZGUgc2VsaW51eF9jb25maWdfcG9saWN5IHNlbGludXhfY3VycmVudF9tb2RlIHNlbGludXhfY3VycmVudF9tb2RlIHNlbGludXhfZW5mb3JjZWQgJyArXG4gICAgICAnc2VsaW51eF9wb2xpY3l2ZXJzaW9uIHNlcmlhbG51bWJlciBzcF8gc3NoZHNha2V5IHNzaGVjZHNha2V5IHNzaHJzYWtleSBzd2FwZW5jcnlwdGVkIHN3YXBmcmVlIHN3YXBzaXplIHRpbWV6b25lIHR5cGUgdW5pcXVlaWQgdXB0aW1lICcgK1xuICAgICAgJ3VwdGltZV9kYXlzIHVwdGltZV9ob3VycyB1cHRpbWVfc2Vjb25kcyB1dWlkIHZpcnR1YWwgdmxhbnMgeGVuZG9tYWlucyB6ZnNfdmVyc2lvbiB6b25lbmFlIHpvbmVzIHpwb29sX3ZlcnNpb24nXG4gIH07XG5cbiAgY29uc3QgQ09NTUVOVCA9IGhsanMuQ09NTUVOVCgnIycsICckJyk7XG5cbiAgY29uc3QgSURFTlRfUkUgPSAnKFtBLVphLXpfXXw6OikoXFxcXHd8OjopKic7XG5cbiAgY29uc3QgVElUTEUgPSBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgYmVnaW46IElERU5UX1JFXG4gIH0pO1xuXG4gIGNvbnN0IFZBUklBQkxFID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICBiZWdpbjogJ1xcXFwkJyArIElERU5UX1JFXG4gIH07XG5cbiAgY29uc3QgU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgIFZBUklBQkxFXG4gICAgXSxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogLycvLFxuICAgICAgICBlbmQ6IC8nL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgIGVuZDogL1wiL1xuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdQdXBwZXQnLFxuICAgIGFsaWFzZXM6IFsgJ3BwJyBdLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBDT01NRU5ULFxuICAgICAgVkFSSUFCTEUsXG4gICAgICBTVFJJTkcsXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdjbGFzcycsXG4gICAgICAgIGVuZDogJ1xcXFx7fDsnLFxuICAgICAgICBpbGxlZ2FsOiAvPS8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgVElUTEUsXG4gICAgICAgICAgQ09NTUVOVFxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnZGVmaW5lJyxcbiAgICAgICAgZW5kOiAvXFx7LyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdzZWN0aW9uJyxcbiAgICAgICAgICAgIGJlZ2luOiBobGpzLklERU5UX1JFLFxuICAgICAgICAgICAgZW5kc1BhcmVudDogdHJ1ZVxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IGhsanMuSURFTlRfUkUgKyAnXFxcXHMrXFxcXHsnLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgZW5kOiAvXFxTLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICAgICAgICAgIGJlZ2luOiBobGpzLklERU5UX1JFXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL1xcey8sXG4gICAgICAgICAgICBlbmQ6IC9cXH0vLFxuICAgICAgICAgICAga2V5d29yZHM6IFBVUFBFVF9LRVlXT1JEUyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIFNUUklORyxcbiAgICAgICAgICAgICAgQ09NTUVOVCxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiAnW2EtekEtWl9dK1xcXFxzKj0+JyxcbiAgICAgICAgICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgICAgICBlbmQ6ICc9PicsXG4gICAgICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnYXR0cicsXG4gICAgICAgICAgICAgICAgICAgIGJlZ2luOiBobGpzLklERU5UX1JFXG4gICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgXVxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgICAgICAgICBiZWdpbjogJyhcXFxcYjBbMC03X10rKXwoXFxcXGIweFswLTlhLWZBLUZfXSspfChcXFxcYlsxLTldWzAtOV9dKihcXFxcLlswLTlfXSspPyl8WzBfXVxcXFxiJyxcbiAgICAgICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgVkFSSUFCTEVcbiAgICAgICAgICAgIF1cbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBwdXBwZXQ7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=