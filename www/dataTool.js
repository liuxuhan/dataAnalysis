! function(e, t) { "object" == typeof exports && "undefined" != typeof module ? t(exports, require("echarts")) : "function" == typeof define && define.amd ? define(["exports", "echarts"], t) : t(e.dataTool = {}, e.echarts) }(this, function(e, t) { "use strict";

    function r(e) { return e ? t.util.map(l(e, "attribute"), function(e) { return { id: o(e, "id"), title: o(e, "title"), type: o(e, "type") } }) : [] }

    function n(e, r) { return e ? t.util.map(l(e, "node"), function(e) { var t = { id: o(e, "id"), name: o(e, "label"), itemStyle: { normal: {} } },
                n = i(e, "viz:size"),
                a = i(e, "viz:position"),
                u = i(e, "viz:color"),
                s = i(e, "attvalues"); if (n && (t.symbolSize = parseFloat(o(n, "value"))), a && (t.x = parseFloat(o(a, "x")), t.y = parseFloat(o(a, "y"))), u && (t.itemStyle.normal.color = "rgb(" + [0 | o(u, "r"), 0 | o(u, "g"), 0 | o(u, "b")].join(",") + ")"), s) { var f = l(s, "attvalue");
                t.attributes = {}; for (var c = 0; c < f.length; c++) { var p = f[c],
                        v = o(p, "for"),
                        d = o(p, "value"),
                        g = r[v]; if (g) { switch (g.type) {
                            case "integer":
                            case "long":
                                d = parseInt(d, 10); break;
                            case "float":
                            case "double":
                                d = parseFloat(d); break;
                            case "boolean":
                                d = "true" == d.toLowerCase() } t.attributes[v] = d } } } return t }) : [] }

    function a(e) { return e ? t.util.map(l(e, "edge"), function(e) { var t = { id: o(e, "id"), name: o(e, "label"), source: o(e, "source"), target: o(e, "target"), lineStyle: { normal: {} } },
                r = t.lineStyle.normal,
                n = i(e, "viz:thickness"),
                a = i(e, "viz:color"); return n && (r.width = parseFloat(n.getAttribute("value"))), a && (r.color = "rgb(" + [0 | o(a, "r"), 0 | o(a, "g"), 0 | o(a, "b")].join(",") + ")"), t }) : [] }

    function o(e, t) { return e.getAttribute(t) }

    function i(e, t) { for (var r = e.firstChild; r;) { if (1 == r.nodeType && r.nodeName.toLowerCase() == t.toLowerCase()) return r;
            r = r.nextSibling } return null }

    function l(e, t) { for (var r = e.firstChild, n = []; r;) r.nodeName.toLowerCase() == t.toLowerCase() && n.push(r), r = r.nextSibling; return n } var u = (Object.freeze || Object)({ parse: function(e) { var t; if (!(t = "string" == typeof e ? (new DOMParser).parseFromString(e, "text/xml") : e) || t.getElementsByTagName("parsererror").length) return null; var o = i(t, "gexf"); if (!o) return null; for (var l = i(o, "graph"), u = r(i(l, "attributes")), s = {}, f = 0; f < u.length; f++) s[u[f].id] = u[f]; return { nodes: n(i(l, "nodes"), s), links: a(i(l, "edges")) } } }),
        s = function(e, t) { var r = (e.length - 1) * t + 1,
                n = Math.floor(r),
                a = +e[n - 1],
                o = r - n; return o ? a + o * (e[n] - a) : a };
    e.version = "1.0.0", e.gexf = u, e.prepareBoxplotData = function(e, r) { for (var n = [], a = [], o = [], i = (r = r || []).boundIQR, l = "none" === i || 0 === i, u = 0; u < e.length; u++) { o.push(u + ""); var f = t.number.asc(e[u].slice()),
                c = s(f, .25),
                p = s(f, .5),
                v = s(f, .75),
                d = f[0],
                g = f[f.length - 1],
                b = (null == i ? 1.5 : i) * (v - c),
                h = l ? d : Math.max(d, c - b),
                m = l ? g : Math.min(g, v + b);
            n.push([h, c, p, v, m]); for (var y = 0; y < f.length; y++) { var x = f[y]; if (x < h || x > m) { var w = [u, x]; "vertical" === r.layout && w.reverse(), a.push(w) } } } return { boxData: n, outliers: a, axisData: o } } });