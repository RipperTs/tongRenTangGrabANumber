
var r = require("./sm3"),
    e = r.sm3,
    t = r.hmac;
 function n(r) {
    return r.map((function(r) {
        return 1 === (r = r.toString(16)).length ? "0" + r : r
    })).join("")
}
 function o(r) {
    var e, t, n = [],
        o = r.length;
    o % 2 != 0 && (t = o + 1, r = (e = r).length >= t ? e : new Array(t - e.length + 1).join("0") + e), o = r.length;
    for (var s = 0; s < o; s += 2) n.push(parseInt(r.substr(s, 2), 16));
    return n
}
module.exports = function(r, s) {
    if (r = "string" == typeof r ? function(r) {
            for (var e = [], t = 0, n = r.length; t < n; t++) {
                var o = r.codePointAt(t);
                if (o <= 127) e.push(o);
                else if (o <= 2047) e.push(192 | o >>> 6), e.push(128 | 63 & o);
                else if (o <= 55295 || o >= 57344 && o <= 65535) e.push(224 | o >>> 12), e.push(128 | o >>> 6 & 63), e.push(128 | 63 & o);
                else {
                    if (!(o >= 65536 && o <= 1114111)) throw e.push(o), new Error("input is not supported");
                    t++, e.push(240 | o >>> 18 & 28), e.push(128 | o >>> 12 & 63), e.push(128 | o >>> 6 & 63), e.push(128 | 63 & o)
                }
            }
            return e
        }(r) : Array.prototype.slice.call(r), s) {
        if ("hmac" !== (s.mode || "hmac")) throw new Error("invalid mode");
        var u = s.key;
        if (!u) throw new Error("invalid key");
        return u = "string" == typeof u ? o(u) : Array.prototype.slice.call(u), n(t(r, u))
    }
    return n(e(r))
};