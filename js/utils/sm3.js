
 function r(r, n) {
    for (var t = [], e = ~~(n / 8), o = n % 8, a = 0, c = r.length; a < c; a++) t[a] = (r[(a + e) % c] << o & 255) + (r[(a + e + 1) % c] >>> 8 - o & 255);
    return t
}
 function n(r, n) {
    for (var t = [], e = r.length - 1; e >= 0; e--) t[e] = 255 & (r[e] ^ n[e]);
    return t
}
 function t(r, n) {
    for (var t = [], e = r.length - 1; e >= 0; e--) t[e] = r[e] & n[e] & 255;
    return t
}
 function e(r, n) {
    for (var t = [], e = r.length - 1; e >= 0; e--) t[e] = 255 & (r[e] | n[e]);
    return t
}
 function o(r, n) {
    for (var t = [], e = 0, o = r.length - 1; o >= 0; o--) {
        var a = r[o] + n[o] + e;
        a > 255 ? (e = 1, t[o] = 255 & a) : (e = 0, t[o] = 255 & a)
    }
    return t
}
 function a(t) {
    return n(n(t, r(t, 9)), r(t, 17))
}
 function c(r, o, a, c) {
    return c >= 0 && c <= 15 ? n(n(r, o), a) : e(e(t(r, o), t(r, a)), t(o, a))
}
 function u(r, o, a, c) {
    return c >= 0 && c <= 15 ? n(n(r, o), a) : e(t(r, o), t(function(r) {
        for (var n = [], t = r.length - 1; t >= 0; t--) n[t] = 255 & ~r[t];
        return n
    }(r), a))
}
 function f(t, e) {
    for (var f, l = [], i = [], s = 0; s < 16; s++) {
        var v = 4 * s;
        l.push(e.slice(v, v + 4))
    }
    for (var h = 16; h < 68; h++) l.push(n(n((f = n(n(l[h - 16], l[h - 9]), r(l[h - 3], 15)), n(n(f, r(f, 15)), r(f, 23))), r(l[h - 13], 7)), l[h - 6]));
    for (var g = 0; g < 64; g++) i.push(n(l[g], l[g + 4]));
    for (var p, m, w, y, A = [121, 204, 69, 25], b = [122, 135, 157, 138], I = t.slice(0, 4), d = t.slice(4, 8), x = t.slice(8, 12), S = t.slice(12, 16), j = t.slice(16, 20), k = t.slice(20, 24), q = t.slice(24, 28), z = t.slice(28, 32), B = 0; B < 64; B++) {
        var C = B >= 0 && B <= 15 ? A : b;
        m = n(p = r(o(o(r(I, 12), j), r(C, B)), 7), r(I, 12)), w = o(o(o(c(I, d, x, B), S), m), i[B]), y = o(o(o(u(j, k, q, B), z), p), l[B]), S = x, x = r(d, 9), d = I, I = w, z = q, q = r(k, 19), k = j, j = a(y)
    }
    return n([].concat(I, d, x, S, j, k, q, z), t)
}
 function l(r) {
    var n = 8 * r.length,
        t = n % 512;
    t = t >= 448 ? 512 - t % 448 - 1 : 448 - t - 1;
    for (var e = new Array((t - 7) / 8), o = 0, a = e.length; o < a; o++) e[o] = 0;
    var c = [];
    n = n.toString(2);
    for (var u = 7; u >= 0; u--)
        if (n.length > 8) {
            var l = n.length - 8;
            c[u] = parseInt(n.substr(l), 2), n = n.substr(0, l)
        } else n.length > 0 ? (c[u] = parseInt(n, 2), n = "") : c[u] = 0;
    for (var i = [].concat(r, [128], e, c), s = i.length / 64, v = [115, 128, 22, 111, 73, 20, 178, 185, 23, 36, 66, 215, 218, 138, 6, 0, 169, 111, 48, 188, 22, 49, 56, 170, 227, 141, 238, 77, 176, 251, 14, 78], h = 0; h < s; h++) {
        var g = 64 * h;
        v = f(v, i.slice(g, g + 64))
    }
    return v
}
for (var i = new Array(64), s = new Array(64), v = 0; v < 64; v++) i[v] = 54, s[v] = 92;
module.exports = {
    sm3: l,
    hmac: function(r, t) {
        for (t.length > 64 && (t = l(t)); t.length < 64;) t.push(0);
        var e = n(t, i).concat(r);
        return e = l(e), e = l(e = n(t, s).concat(e))
    }
};