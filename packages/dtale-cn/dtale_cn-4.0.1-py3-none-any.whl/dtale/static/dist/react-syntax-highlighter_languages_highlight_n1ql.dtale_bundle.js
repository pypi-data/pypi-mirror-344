(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_n1ql"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/n1ql.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/n1ql.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
 Language: N1QL
 Author: Andres Täht <andres.taht@gmail.com>
 Contributors: Rene Saarsoo <nene@triin.net>
 Description: Couchbase query language
 Website: https://www.couchbase.com/products/n1ql
 */

function n1ql(hljs) {
  return {
    name: 'N1QL',
    case_insensitive: true,
    contains: [
      {
        beginKeywords:
          'build create index delete drop explain infer|10 insert merge prepare select update upsert|10',
        end: /;/, endsWithParent: true,
        keywords: {
          // Taken from http://developer.couchbase.com/documentation/server/current/n1ql/n1ql-language-reference/reservedwords.html
          keyword:
            'all alter analyze and any array as asc begin between binary boolean break bucket build by call ' +
            'case cast cluster collate collection commit connect continue correlate cover create database ' +
            'dataset datastore declare decrement delete derived desc describe distinct do drop each element ' +
            'else end every except exclude execute exists explain fetch first flatten for force from ' +
            'function grant group gsi having if ignore ilike in include increment index infer inline inner ' +
            'insert intersect into is join key keys keyspace known last left let letting like limit lsm map ' +
            'mapping matched materialized merge minus namespace nest not number object offset on ' +
            'option or order outer over parse partition password path pool prepare primary private privilege ' +
            'procedure public raw realm reduce rename return returning revoke right role rollback satisfies ' +
            'schema select self semi set show some start statistics string system then to transaction trigger ' +
            'truncate under union unique unknown unnest unset update upsert use user using validate value ' +
            'valued values via view when where while with within work xor',
          // Taken from http://developer.couchbase.com/documentation/server/4.5/n1ql/n1ql-language-reference/literals.html
          literal:
            'true false null missing|5',
          // Taken from http://developer.couchbase.com/documentation/server/4.5/n1ql/n1ql-language-reference/functions.html
          built_in:
            'array_agg array_append array_concat array_contains array_count array_distinct array_ifnull array_length ' +
            'array_max array_min array_position array_prepend array_put array_range array_remove array_repeat array_replace ' +
            'array_reverse array_sort array_sum avg count max min sum greatest least ifmissing ifmissingornull ifnull ' +
            'missingif nullif ifinf ifnan ifnanorinf naninf neginfif posinfif clock_millis clock_str date_add_millis ' +
            'date_add_str date_diff_millis date_diff_str date_part_millis date_part_str date_trunc_millis date_trunc_str ' +
            'duration_to_str millis str_to_millis millis_to_str millis_to_utc millis_to_zone_name now_millis now_str ' +
            'str_to_duration str_to_utc str_to_zone_name decode_json encode_json encoded_size poly_length base64 base64_encode ' +
            'base64_decode meta uuid abs acos asin atan atan2 ceil cos degrees e exp ln log floor pi power radians random ' +
            'round sign sin sqrt tan trunc object_length object_names object_pairs object_inner_pairs object_values ' +
            'object_inner_values object_add object_put object_remove object_unwrap regexp_contains regexp_like regexp_position ' +
            'regexp_replace contains initcap length lower ltrim position repeat replace rtrim split substr title trim upper ' +
            'isarray isatom isboolean isnumber isobject isstring type toarray toatom toboolean tonumber toobject tostring'
        },
        contains: [
          {
            className: 'string',
            begin: '\'', end: '\'',
            contains: [hljs.BACKSLASH_ESCAPE]
          },
          {
            className: 'string',
            begin: '"', end: '"',
            contains: [hljs.BACKSLASH_ESCAPE]
          },
          {
            className: 'symbol',
            begin: '`', end: '`',
            contains: [hljs.BACKSLASH_ESCAPE],
            relevance: 2
          },
          hljs.C_NUMBER_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      hljs.C_BLOCK_COMMENT_MODE
    ]
  };
}

module.exports = n1ql;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbjFxbC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvbjFxbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuIExhbmd1YWdlOiBOMVFMXG4gQXV0aG9yOiBBbmRyZXMgVMOkaHQgPGFuZHJlcy50YWh0QGdtYWlsLmNvbT5cbiBDb250cmlidXRvcnM6IFJlbmUgU2FhcnNvbyA8bmVuZUB0cmlpbi5uZXQ+XG4gRGVzY3JpcHRpb246IENvdWNoYmFzZSBxdWVyeSBsYW5ndWFnZVxuIFdlYnNpdGU6IGh0dHBzOi8vd3d3LmNvdWNoYmFzZS5jb20vcHJvZHVjdHMvbjFxbFxuICovXG5cbmZ1bmN0aW9uIG4xcWwoaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdOMVFMJyxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6XG4gICAgICAgICAgJ2J1aWxkIGNyZWF0ZSBpbmRleCBkZWxldGUgZHJvcCBleHBsYWluIGluZmVyfDEwIGluc2VydCBtZXJnZSBwcmVwYXJlIHNlbGVjdCB1cGRhdGUgdXBzZXJ0fDEwJyxcbiAgICAgICAgZW5kOiAvOy8sIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgICAgICBrZXl3b3Jkczoge1xuICAgICAgICAgIC8vIFRha2VuIGZyb20gaHR0cDovL2RldmVsb3Blci5jb3VjaGJhc2UuY29tL2RvY3VtZW50YXRpb24vc2VydmVyL2N1cnJlbnQvbjFxbC9uMXFsLWxhbmd1YWdlLXJlZmVyZW5jZS9yZXNlcnZlZHdvcmRzLmh0bWxcbiAgICAgICAgICBrZXl3b3JkOlxuICAgICAgICAgICAgJ2FsbCBhbHRlciBhbmFseXplIGFuZCBhbnkgYXJyYXkgYXMgYXNjIGJlZ2luIGJldHdlZW4gYmluYXJ5IGJvb2xlYW4gYnJlYWsgYnVja2V0IGJ1aWxkIGJ5IGNhbGwgJyArXG4gICAgICAgICAgICAnY2FzZSBjYXN0IGNsdXN0ZXIgY29sbGF0ZSBjb2xsZWN0aW9uIGNvbW1pdCBjb25uZWN0IGNvbnRpbnVlIGNvcnJlbGF0ZSBjb3ZlciBjcmVhdGUgZGF0YWJhc2UgJyArXG4gICAgICAgICAgICAnZGF0YXNldCBkYXRhc3RvcmUgZGVjbGFyZSBkZWNyZW1lbnQgZGVsZXRlIGRlcml2ZWQgZGVzYyBkZXNjcmliZSBkaXN0aW5jdCBkbyBkcm9wIGVhY2ggZWxlbWVudCAnICtcbiAgICAgICAgICAgICdlbHNlIGVuZCBldmVyeSBleGNlcHQgZXhjbHVkZSBleGVjdXRlIGV4aXN0cyBleHBsYWluIGZldGNoIGZpcnN0IGZsYXR0ZW4gZm9yIGZvcmNlIGZyb20gJyArXG4gICAgICAgICAgICAnZnVuY3Rpb24gZ3JhbnQgZ3JvdXAgZ3NpIGhhdmluZyBpZiBpZ25vcmUgaWxpa2UgaW4gaW5jbHVkZSBpbmNyZW1lbnQgaW5kZXggaW5mZXIgaW5saW5lIGlubmVyICcgK1xuICAgICAgICAgICAgJ2luc2VydCBpbnRlcnNlY3QgaW50byBpcyBqb2luIGtleSBrZXlzIGtleXNwYWNlIGtub3duIGxhc3QgbGVmdCBsZXQgbGV0dGluZyBsaWtlIGxpbWl0IGxzbSBtYXAgJyArXG4gICAgICAgICAgICAnbWFwcGluZyBtYXRjaGVkIG1hdGVyaWFsaXplZCBtZXJnZSBtaW51cyBuYW1lc3BhY2UgbmVzdCBub3QgbnVtYmVyIG9iamVjdCBvZmZzZXQgb24gJyArXG4gICAgICAgICAgICAnb3B0aW9uIG9yIG9yZGVyIG91dGVyIG92ZXIgcGFyc2UgcGFydGl0aW9uIHBhc3N3b3JkIHBhdGggcG9vbCBwcmVwYXJlIHByaW1hcnkgcHJpdmF0ZSBwcml2aWxlZ2UgJyArXG4gICAgICAgICAgICAncHJvY2VkdXJlIHB1YmxpYyByYXcgcmVhbG0gcmVkdWNlIHJlbmFtZSByZXR1cm4gcmV0dXJuaW5nIHJldm9rZSByaWdodCByb2xlIHJvbGxiYWNrIHNhdGlzZmllcyAnICtcbiAgICAgICAgICAgICdzY2hlbWEgc2VsZWN0IHNlbGYgc2VtaSBzZXQgc2hvdyBzb21lIHN0YXJ0IHN0YXRpc3RpY3Mgc3RyaW5nIHN5c3RlbSB0aGVuIHRvIHRyYW5zYWN0aW9uIHRyaWdnZXIgJyArXG4gICAgICAgICAgICAndHJ1bmNhdGUgdW5kZXIgdW5pb24gdW5pcXVlIHVua25vd24gdW5uZXN0IHVuc2V0IHVwZGF0ZSB1cHNlcnQgdXNlIHVzZXIgdXNpbmcgdmFsaWRhdGUgdmFsdWUgJyArXG4gICAgICAgICAgICAndmFsdWVkIHZhbHVlcyB2aWEgdmlldyB3aGVuIHdoZXJlIHdoaWxlIHdpdGggd2l0aGluIHdvcmsgeG9yJyxcbiAgICAgICAgICAvLyBUYWtlbiBmcm9tIGh0dHA6Ly9kZXZlbG9wZXIuY291Y2hiYXNlLmNvbS9kb2N1bWVudGF0aW9uL3NlcnZlci80LjUvbjFxbC9uMXFsLWxhbmd1YWdlLXJlZmVyZW5jZS9saXRlcmFscy5odG1sXG4gICAgICAgICAgbGl0ZXJhbDpcbiAgICAgICAgICAgICd0cnVlIGZhbHNlIG51bGwgbWlzc2luZ3w1JyxcbiAgICAgICAgICAvLyBUYWtlbiBmcm9tIGh0dHA6Ly9kZXZlbG9wZXIuY291Y2hiYXNlLmNvbS9kb2N1bWVudGF0aW9uL3NlcnZlci80LjUvbjFxbC9uMXFsLWxhbmd1YWdlLXJlZmVyZW5jZS9mdW5jdGlvbnMuaHRtbFxuICAgICAgICAgIGJ1aWx0X2luOlxuICAgICAgICAgICAgJ2FycmF5X2FnZyBhcnJheV9hcHBlbmQgYXJyYXlfY29uY2F0IGFycmF5X2NvbnRhaW5zIGFycmF5X2NvdW50IGFycmF5X2Rpc3RpbmN0IGFycmF5X2lmbnVsbCBhcnJheV9sZW5ndGggJyArXG4gICAgICAgICAgICAnYXJyYXlfbWF4IGFycmF5X21pbiBhcnJheV9wb3NpdGlvbiBhcnJheV9wcmVwZW5kIGFycmF5X3B1dCBhcnJheV9yYW5nZSBhcnJheV9yZW1vdmUgYXJyYXlfcmVwZWF0IGFycmF5X3JlcGxhY2UgJyArXG4gICAgICAgICAgICAnYXJyYXlfcmV2ZXJzZSBhcnJheV9zb3J0IGFycmF5X3N1bSBhdmcgY291bnQgbWF4IG1pbiBzdW0gZ3JlYXRlc3QgbGVhc3QgaWZtaXNzaW5nIGlmbWlzc2luZ29ybnVsbCBpZm51bGwgJyArXG4gICAgICAgICAgICAnbWlzc2luZ2lmIG51bGxpZiBpZmluZiBpZm5hbiBpZm5hbm9yaW5mIG5hbmluZiBuZWdpbmZpZiBwb3NpbmZpZiBjbG9ja19taWxsaXMgY2xvY2tfc3RyIGRhdGVfYWRkX21pbGxpcyAnICtcbiAgICAgICAgICAgICdkYXRlX2FkZF9zdHIgZGF0ZV9kaWZmX21pbGxpcyBkYXRlX2RpZmZfc3RyIGRhdGVfcGFydF9taWxsaXMgZGF0ZV9wYXJ0X3N0ciBkYXRlX3RydW5jX21pbGxpcyBkYXRlX3RydW5jX3N0ciAnICtcbiAgICAgICAgICAgICdkdXJhdGlvbl90b19zdHIgbWlsbGlzIHN0cl90b19taWxsaXMgbWlsbGlzX3RvX3N0ciBtaWxsaXNfdG9fdXRjIG1pbGxpc190b196b25lX25hbWUgbm93X21pbGxpcyBub3dfc3RyICcgK1xuICAgICAgICAgICAgJ3N0cl90b19kdXJhdGlvbiBzdHJfdG9fdXRjIHN0cl90b196b25lX25hbWUgZGVjb2RlX2pzb24gZW5jb2RlX2pzb24gZW5jb2RlZF9zaXplIHBvbHlfbGVuZ3RoIGJhc2U2NCBiYXNlNjRfZW5jb2RlICcgK1xuICAgICAgICAgICAgJ2Jhc2U2NF9kZWNvZGUgbWV0YSB1dWlkIGFicyBhY29zIGFzaW4gYXRhbiBhdGFuMiBjZWlsIGNvcyBkZWdyZWVzIGUgZXhwIGxuIGxvZyBmbG9vciBwaSBwb3dlciByYWRpYW5zIHJhbmRvbSAnICtcbiAgICAgICAgICAgICdyb3VuZCBzaWduIHNpbiBzcXJ0IHRhbiB0cnVuYyBvYmplY3RfbGVuZ3RoIG9iamVjdF9uYW1lcyBvYmplY3RfcGFpcnMgb2JqZWN0X2lubmVyX3BhaXJzIG9iamVjdF92YWx1ZXMgJyArXG4gICAgICAgICAgICAnb2JqZWN0X2lubmVyX3ZhbHVlcyBvYmplY3RfYWRkIG9iamVjdF9wdXQgb2JqZWN0X3JlbW92ZSBvYmplY3RfdW53cmFwIHJlZ2V4cF9jb250YWlucyByZWdleHBfbGlrZSByZWdleHBfcG9zaXRpb24gJyArXG4gICAgICAgICAgICAncmVnZXhwX3JlcGxhY2UgY29udGFpbnMgaW5pdGNhcCBsZW5ndGggbG93ZXIgbHRyaW0gcG9zaXRpb24gcmVwZWF0IHJlcGxhY2UgcnRyaW0gc3BsaXQgc3Vic3RyIHRpdGxlIHRyaW0gdXBwZXIgJyArXG4gICAgICAgICAgICAnaXNhcnJheSBpc2F0b20gaXNib29sZWFuIGlzbnVtYmVyIGlzb2JqZWN0IGlzc3RyaW5nIHR5cGUgdG9hcnJheSB0b2F0b20gdG9ib29sZWFuIHRvbnVtYmVyIHRvb2JqZWN0IHRvc3RyaW5nJ1xuICAgICAgICB9LFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgICAgICBiZWdpbjogJ1xcJycsIGVuZDogJ1xcJycsXG4gICAgICAgICAgICBjb250YWluczogW2hsanMuQkFDS1NMQVNIX0VTQ0FQRV1cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgICAgICBiZWdpbjogJ1wiJywgZW5kOiAnXCInLFxuICAgICAgICAgICAgY29udGFpbnM6IFtobGpzLkJBQ0tTTEFTSF9FU0NBUEVdXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgICAgICAgICAgYmVnaW46ICdgJywgZW5kOiAnYCcsXG4gICAgICAgICAgICBjb250YWluczogW2hsanMuQkFDS1NMQVNIX0VTQ0FQRV0sXG4gICAgICAgICAgICByZWxldmFuY2U6IDJcbiAgICAgICAgICB9LFxuICAgICAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IG4xcWw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=