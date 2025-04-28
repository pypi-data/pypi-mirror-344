import { i as qt, a as ne, r as Yt, w as le, g as Qt, c as Y, b as Ae } from "./Index-Bau7eqkM.js";
const I = window.ms_globals.React, h = window.ms_globals.React, Vt = window.ms_globals.React.version, Wt = window.ms_globals.React.forwardRef, vt = window.ms_globals.React.useRef, Ut = window.ms_globals.React.useState, Gt = window.ms_globals.React.useEffect, Kt = window.ms_globals.React.useCallback, de = window.ms_globals.React.useMemo, Le = window.ms_globals.ReactDOM.createPortal, Jt = window.ms_globals.internalContext.useContextPropsContext, qe = window.ms_globals.internalContext.ContextPropsProvider, xt = window.ms_globals.createItemsContext.createItemsContext, Zt = window.ms_globals.antd.ConfigProvider, $e = window.ms_globals.antd.theme, er = window.ms_globals.antd.Avatar, oe = window.ms_globals.antdCssinjs.unit, Pe = window.ms_globals.antdCssinjs.token2CSSVar, Ye = window.ms_globals.antdCssinjs.useStyleRegister, tr = window.ms_globals.antdCssinjs.useCSSVarRegister, rr = window.ms_globals.antdCssinjs.createTheme, nr = window.ms_globals.antdCssinjs.useCacheToken, St = window.ms_globals.antdCssinjs.Keyframes;
var or = /\s/;
function sr(e) {
  for (var t = e.length; t-- && or.test(e.charAt(t)); )
    ;
  return t;
}
var ir = /^\s+/;
function ar(e) {
  return e && e.slice(0, sr(e) + 1).replace(ir, "");
}
var Qe = NaN, lr = /^[-+]0x[0-9a-f]+$/i, cr = /^0b[01]+$/i, ur = /^0o[0-7]+$/i, fr = parseInt;
function Je(e) {
  if (typeof e == "number")
    return e;
  if (qt(e))
    return Qe;
  if (ne(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = ne(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = ar(e);
  var n = cr.test(e);
  return n || ur.test(e) ? fr(e.slice(2), n ? 2 : 8) : lr.test(e) ? Qe : +e;
}
var Oe = function() {
  return Yt.Date.now();
}, dr = "Expected a function", hr = Math.max, gr = Math.min;
function mr(e, t, n) {
  var o, r, s, i, a, l, c = 0, u = !1, f = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(dr);
  t = Je(t) || 0, ne(n) && (u = !!n.leading, f = "maxWait" in n, s = f ? hr(Je(n.maxWait) || 0, t) : s, d = "trailing" in n ? !!n.trailing : d);
  function g(x) {
    var M = o, P = r;
    return o = r = void 0, c = x, i = e.apply(P, M), i;
  }
  function b(x) {
    return c = x, a = setTimeout(p, t), u ? g(x) : i;
  }
  function v(x) {
    var M = x - l, P = x - c, S = t - M;
    return f ? gr(S, s - P) : S;
  }
  function m(x) {
    var M = x - l, P = x - c;
    return l === void 0 || M >= t || M < 0 || f && P >= s;
  }
  function p() {
    var x = Oe();
    if (m(x))
      return w(x);
    a = setTimeout(p, v(x));
  }
  function w(x) {
    return a = void 0, d && o ? g(x) : (o = r = void 0, i);
  }
  function k() {
    a !== void 0 && clearTimeout(a), c = 0, o = l = r = a = void 0;
  }
  function y() {
    return a === void 0 ? i : w(Oe());
  }
  function C() {
    var x = Oe(), M = m(x);
    if (o = arguments, r = this, l = x, M) {
      if (a === void 0)
        return b(l);
      if (f)
        return clearTimeout(a), a = setTimeout(p, t), g(l);
    }
    return a === void 0 && (a = setTimeout(p, t)), i;
  }
  return C.cancel = k, C.flush = y, C;
}
var Ct = {
  exports: {}
}, me = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var pr = h, br = Symbol.for("react.element"), yr = Symbol.for("react.fragment"), vr = Object.prototype.hasOwnProperty, xr = pr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Sr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function _t(e, t, n) {
  var o, r = {}, s = null, i = null;
  n !== void 0 && (s = "" + n), t.key !== void 0 && (s = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (o in t) vr.call(t, o) && !Sr.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: br,
    type: e,
    key: s,
    ref: i,
    props: r,
    _owner: xr.current
  };
}
me.Fragment = yr;
me.jsx = _t;
me.jsxs = _t;
Ct.exports = me;
var H = Ct.exports;
const {
  SvelteComponent: Cr,
  assign: Ze,
  binding_callbacks: et,
  check_outros: _r,
  children: wt,
  claim_element: Tt,
  claim_space: wr,
  component_subscribe: tt,
  compute_slots: Tr,
  create_slot: Er,
  detach: Q,
  element: Et,
  empty: rt,
  exclude_internal_props: nt,
  get_all_dirty_from_scope: Mr,
  get_slot_changes: Pr,
  group_outros: Or,
  init: Ir,
  insert_hydration: ce,
  safe_not_equal: Rr,
  set_custom_element_data: Mt,
  space: kr,
  transition_in: ue,
  transition_out: De,
  update_slot_base: jr
} = window.__gradio__svelte__internal, {
  beforeUpdate: Lr,
  getContext: $r,
  onDestroy: Dr,
  setContext: Hr
} = window.__gradio__svelte__internal;
function ot(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = Er(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Et("svelte-slot"), r && r.c(), this.h();
    },
    l(s) {
      t = Tt(s, "SVELTE-SLOT", {
        class: !0
      });
      var i = wt(t);
      r && r.l(i), i.forEach(Q), this.h();
    },
    h() {
      Mt(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      ce(s, t, i), r && r.m(t, null), e[9](t), n = !0;
    },
    p(s, i) {
      r && r.p && (!n || i & /*$$scope*/
      64) && jr(
        r,
        o,
        s,
        /*$$scope*/
        s[6],
        n ? Pr(
          o,
          /*$$scope*/
          s[6],
          i,
          null
        ) : Mr(
          /*$$scope*/
          s[6]
        ),
        null
      );
    },
    i(s) {
      n || (ue(r, s), n = !0);
    },
    o(s) {
      De(r, s), n = !1;
    },
    d(s) {
      s && Q(t), r && r.d(s), e[9](null);
    }
  };
}
function Br(e) {
  let t, n, o, r, s = (
    /*$$slots*/
    e[4].default && ot(e)
  );
  return {
    c() {
      t = Et("react-portal-target"), n = kr(), s && s.c(), o = rt(), this.h();
    },
    l(i) {
      t = Tt(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), wt(t).forEach(Q), n = wr(i), s && s.l(i), o = rt(), this.h();
    },
    h() {
      Mt(t, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      ce(i, t, a), e[8](t), ce(i, n, a), s && s.m(i, a), ce(i, o, a), r = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? s ? (s.p(i, a), a & /*$$slots*/
      16 && ue(s, 1)) : (s = ot(i), s.c(), ue(s, 1), s.m(o.parentNode, o)) : s && (Or(), De(s, 1, 1, () => {
        s = null;
      }), _r());
    },
    i(i) {
      r || (ue(s), r = !0);
    },
    o(i) {
      De(s), r = !1;
    },
    d(i) {
      i && (Q(t), Q(n), Q(o)), e[8](null), s && s.d(i);
    }
  };
}
function st(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function zr(e, t, n) {
  let o, r, {
    $$slots: s = {},
    $$scope: i
  } = t;
  const a = Tr(s);
  let {
    svelteInit: l
  } = t;
  const c = le(st(t)), u = le();
  tt(e, u, (y) => n(0, o = y));
  const f = le();
  tt(e, f, (y) => n(1, r = y));
  const d = [], g = $r("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: v,
    subSlotIndex: m
  } = Qt() || {}, p = l({
    parent: g,
    props: c,
    target: u,
    slot: f,
    slotKey: b,
    slotIndex: v,
    subSlotIndex: m,
    onDestroy(y) {
      d.push(y);
    }
  });
  Hr("$$ms-gr-react-wrapper", p), Lr(() => {
    c.set(st(t));
  }), Dr(() => {
    d.forEach((y) => y());
  });
  function w(y) {
    et[y ? "unshift" : "push"](() => {
      o = y, u.set(o);
    });
  }
  function k(y) {
    et[y ? "unshift" : "push"](() => {
      r = y, f.set(r);
    });
  }
  return e.$$set = (y) => {
    n(17, t = Ze(Ze({}, t), nt(y))), "svelteInit" in y && n(5, l = y.svelteInit), "$$scope" in y && n(6, i = y.$$scope);
  }, t = nt(t), [o, r, u, f, a, l, i, s, w, k];
}
class Ar extends Cr {
  constructor(t) {
    super(), Ir(this, t, zr, Br, Rr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ho
} = window.__gradio__svelte__internal, it = window.ms_globals.rerender, Ie = window.ms_globals.tree;
function Fr(e, t = {}) {
  function n(o) {
    const r = le(), s = new Ar({
      ...o,
      props: {
        svelteInit(i) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: i.props,
            slot: i.slot,
            target: i.target,
            slotIndex: i.slotIndex,
            subSlotIndex: i.subSlotIndex,
            ignore: t.ignore,
            slotKey: i.slotKey,
            nodes: []
          }, l = i.parent ?? Ie;
          return l.nodes = [...l.nodes, a], it({
            createPortal: Le,
            node: Ie
          }), i.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== r), it({
              createPortal: Le,
              node: Ie
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Xr = "1.1.0", Nr = /* @__PURE__ */ h.createContext({}), Vr = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Wr = (e) => {
  const t = h.useContext(Nr);
  return h.useMemo(() => ({
    ...Vr,
    ...t[e]
  }), [t[e]]);
};
function se() {
  return se = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (e[o] = n[o]);
    }
    return e;
  }, se.apply(null, arguments);
}
function he() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = h.useContext(Zt.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function Pt(e) {
  var t = I.useRef();
  t.current = e;
  var n = I.useCallback(function() {
    for (var o, r = arguments.length, s = new Array(r), i = 0; i < r; i++)
      s[i] = arguments[i];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(s));
  }, []);
  return n;
}
function Ur(e) {
  if (Array.isArray(e)) return e;
}
function Gr(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, s, i, a = [], l = !0, c = !1;
    try {
      if (s = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = s.call(n)).done) && (a.push(o.value), a.length !== t); l = !0) ;
    } catch (u) {
      c = !0, r = u;
    } finally {
      try {
        if (!l && n.return != null && (i = n.return(), Object(i) !== i)) return;
      } finally {
        if (c) throw r;
      }
    }
    return a;
  }
}
function at(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function Kr(e, t) {
  if (e) {
    if (typeof e == "string") return at(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? at(e, t) : void 0;
  }
}
function qr() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function fe(e, t) {
  return Ur(e) || Gr(e, t) || Kr(e, t) || qr();
}
function Yr() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var lt = Yr() ? I.useLayoutEffect : I.useEffect, Qr = function(t, n) {
  var o = I.useRef(!0);
  lt(function() {
    return t(o.current);
  }, n), lt(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
};
function N(e) {
  "@babel/helpers - typeof";
  return N = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, N(e);
}
var E = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Fe = Symbol.for("react.element"), Xe = Symbol.for("react.portal"), pe = Symbol.for("react.fragment"), be = Symbol.for("react.strict_mode"), ye = Symbol.for("react.profiler"), ve = Symbol.for("react.provider"), xe = Symbol.for("react.context"), Jr = Symbol.for("react.server_context"), Se = Symbol.for("react.forward_ref"), Ce = Symbol.for("react.suspense"), _e = Symbol.for("react.suspense_list"), we = Symbol.for("react.memo"), Te = Symbol.for("react.lazy"), Zr = Symbol.for("react.offscreen"), Ot;
Ot = Symbol.for("react.module.reference");
function B(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Fe:
        switch (e = e.type, e) {
          case pe:
          case ye:
          case be:
          case Ce:
          case _e:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Jr:
              case xe:
              case Se:
              case Te:
              case we:
              case ve:
                return e;
              default:
                return t;
            }
        }
      case Xe:
        return t;
    }
  }
}
E.ContextConsumer = xe;
E.ContextProvider = ve;
E.Element = Fe;
E.ForwardRef = Se;
E.Fragment = pe;
E.Lazy = Te;
E.Memo = we;
E.Portal = Xe;
E.Profiler = ye;
E.StrictMode = be;
E.Suspense = Ce;
E.SuspenseList = _e;
E.isAsyncMode = function() {
  return !1;
};
E.isConcurrentMode = function() {
  return !1;
};
E.isContextConsumer = function(e) {
  return B(e) === xe;
};
E.isContextProvider = function(e) {
  return B(e) === ve;
};
E.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Fe;
};
E.isForwardRef = function(e) {
  return B(e) === Se;
};
E.isFragment = function(e) {
  return B(e) === pe;
};
E.isLazy = function(e) {
  return B(e) === Te;
};
E.isMemo = function(e) {
  return B(e) === we;
};
E.isPortal = function(e) {
  return B(e) === Xe;
};
E.isProfiler = function(e) {
  return B(e) === ye;
};
E.isStrictMode = function(e) {
  return B(e) === be;
};
E.isSuspense = function(e) {
  return B(e) === Ce;
};
E.isSuspenseList = function(e) {
  return B(e) === _e;
};
E.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === pe || e === ye || e === be || e === Ce || e === _e || e === Zr || typeof e == "object" && e !== null && (e.$$typeof === Te || e.$$typeof === we || e.$$typeof === ve || e.$$typeof === xe || e.$$typeof === Se || e.$$typeof === Ot || e.getModuleId !== void 0);
};
E.typeOf = B;
Number(Vt.split(".")[0]);
function en(e, t) {
  if (N(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (N(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function It(e) {
  var t = en(e, "string");
  return N(t) == "symbol" ? t : t + "";
}
function R(e, t, n) {
  return (t = It(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function ct(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function D(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? ct(Object(n), !0).forEach(function(o) {
      R(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : ct(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function Ee(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function tn(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, It(o.key), o);
  }
}
function Me(e, t, n) {
  return t && tn(e.prototype, t), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function He(e, t) {
  return He = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, He(e, t);
}
function Rt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && He(e, t);
}
function ge(e) {
  return ge = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, ge(e);
}
function kt() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (kt = function() {
    return !!e;
  })();
}
function re(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function rn(e, t) {
  if (t && (N(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return re(e);
}
function jt(e) {
  var t = kt();
  return function() {
    var n, o = ge(e);
    if (t) {
      var r = ge(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return rn(this, n);
  };
}
var Lt = /* @__PURE__ */ Me(function e() {
  Ee(this, e);
}), $t = "CALC_UNIT", nn = new RegExp($t, "g");
function Re(e) {
  return typeof e == "number" ? "".concat(e).concat($t) : e;
}
var on = /* @__PURE__ */ function(e) {
  Rt(n, e);
  var t = jt(n);
  function n(o, r) {
    var s;
    Ee(this, n), s = t.call(this), R(re(s), "result", ""), R(re(s), "unitlessCssVar", void 0), R(re(s), "lowPriority", void 0);
    var i = N(o);
    return s.unitlessCssVar = r, o instanceof n ? s.result = "(".concat(o.result, ")") : i === "number" ? s.result = Re(o) : i === "string" && (s.result = o), s;
  }
  return Me(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(Re(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(Re(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " * ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " * ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " / ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " / ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(r) {
      return this.lowPriority || r ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(r) {
      var s = this, i = r || {}, a = i.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(c) {
        return s.result.includes(c);
      }) && (l = !1), this.result = this.result.replace(nn, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Lt), sn = /* @__PURE__ */ function(e) {
  Rt(n, e);
  var t = jt(n);
  function n(o) {
    var r;
    return Ee(this, n), r = t.call(this), R(re(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return Me(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result += r.result : typeof r == "number" && (this.result += r), this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result -= r.result : typeof r == "number" && (this.result -= r), this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return r instanceof n ? this.result *= r.result : typeof r == "number" && (this.result *= r), this;
    }
  }, {
    key: "div",
    value: function(r) {
      return r instanceof n ? this.result /= r.result : typeof r == "number" && (this.result /= r), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(Lt), an = function(t, n) {
  var o = t === "css" ? on : sn;
  return function(r) {
    return new o(r, n);
  };
}, ut = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ft(e, t, n, o) {
  var r = D({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var s = o.deprecatedTokens;
    s.forEach(function(a) {
      var l = fe(a, 2), c = l[0], u = l[1];
      if (r != null && r[c] || r != null && r[u]) {
        var f;
        (f = r[u]) !== null && f !== void 0 || (r[u] = r == null ? void 0 : r[c]);
      }
    });
  }
  var i = D(D({}, n), r);
  return Object.keys(i).forEach(function(a) {
    i[a] === t[a] && delete i[a];
  }), i;
}
var Dt = typeof CSSINJS_STATISTIC < "u", Be = !0;
function Ne() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!Dt)
    return Object.assign.apply(Object, [{}].concat(t));
  Be = !1;
  var o = {};
  return t.forEach(function(r) {
    if (N(r) === "object") {
      var s = Object.keys(r);
      s.forEach(function(i) {
        Object.defineProperty(o, i, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[i];
          }
        });
      });
    }
  }), Be = !0, o;
}
var dt = {};
function ln() {
}
var cn = function(t) {
  var n, o = t, r = ln;
  return Dt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(i, a) {
      if (Be) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return i[a];
    }
  }), r = function(i, a) {
    var l;
    dt[i] = {
      global: Array.from(n),
      component: D(D({}, (l = dt[i]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function ht(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Ne(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function un(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(s) {
        return oe(s);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(s) {
        return oe(s);
      }).join(","), ")");
    }
  };
}
var fn = 1e3 * 60 * 10, dn = /* @__PURE__ */ function() {
  function e() {
    Ee(this, e), R(this, "map", /* @__PURE__ */ new Map()), R(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), R(this, "nextID", 0), R(this, "lastAccessBeat", /* @__PURE__ */ new Map()), R(this, "accessBeat", 0);
  }
  return Me(e, [{
    key: "set",
    value: function(n, o) {
      this.clear();
      var r = this.getCompositeKey(n);
      this.map.set(r, o), this.lastAccessBeat.set(r, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var o = this.getCompositeKey(n), r = this.map.get(o);
      return this.lastAccessBeat.set(o, Date.now()), this.accessBeat += 1, r;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var o = this, r = n.map(function(s) {
        return s && N(s) === "object" ? "obj_".concat(o.getObjectID(s)) : "".concat(N(s), "_").concat(s);
      });
      return r.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var o = this.nextID;
      return this.objectIDMap.set(n, o), this.nextID += 1, o;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var o = Date.now();
        this.lastAccessBeat.forEach(function(r, s) {
          o - r > fn && (n.map.delete(s), n.lastAccessBeat.delete(s));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), gt = new dn();
function hn(e, t) {
  return h.useMemo(function() {
    var n = gt.get(t);
    if (n)
      return n;
    var o = e();
    return gt.set(t, o), o;
  }, t);
}
var gn = function() {
  return {};
};
function mn(e) {
  var t = e.useCSP, n = t === void 0 ? gn : t, o = e.useToken, r = e.usePrefix, s = e.getResetStyles, i = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, g, b, v) {
    var m = Array.isArray(d) ? d[0] : d;
    function p(P) {
      return "".concat(String(m)).concat(P.slice(0, 1).toUpperCase()).concat(P.slice(1));
    }
    var w = (v == null ? void 0 : v.unitless) || {}, k = typeof a == "function" ? a(d) : {}, y = D(D({}, k), {}, R({}, p("zIndexPopup"), !0));
    Object.keys(w).forEach(function(P) {
      y[p(P)] = w[P];
    });
    var C = D(D({}, v), {}, {
      unitless: y,
      prefixToken: p
    }), x = u(d, g, b, C), M = c(m, b, C);
    return function(P) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : P, O = x(P, S), z = fe(O, 2), L = z[1], A = M(S), _ = fe(A, 2), T = _[0], j = _[1];
      return [T, L, j];
    };
  }
  function c(d, g, b) {
    var v = b.unitless, m = b.injectStyle, p = m === void 0 ? !0 : m, w = b.prefixToken, k = b.ignore, y = function(M) {
      var P = M.rootCls, S = M.cssVar, O = S === void 0 ? {} : S, z = o(), L = z.realToken;
      return tr({
        path: [d],
        prefix: O.prefix,
        key: O.key,
        unitless: v,
        ignore: k,
        token: L,
        scope: P
      }, function() {
        var A = ht(d, L, g), _ = ft(d, L, A, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(A).forEach(function(T) {
          _[w(T)] = _[T], delete _[T];
        }), _;
      }), null;
    }, C = function(M) {
      var P = o(), S = P.cssVar;
      return [function(O) {
        return p && S ? /* @__PURE__ */ h.createElement(h.Fragment, null, /* @__PURE__ */ h.createElement(y, {
          rootCls: M,
          cssVar: S,
          component: d
        }), O) : O;
      }, S == null ? void 0 : S.key];
    };
    return C;
  }
  function u(d, g, b) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(d) ? d : [d, d], p = fe(m, 1), w = p[0], k = m.join("-"), y = e.layer || {
      name: "antd"
    };
    return function(C) {
      var x = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, M = o(), P = M.theme, S = M.realToken, O = M.hashId, z = M.token, L = M.cssVar, A = r(), _ = A.rootPrefixCls, T = A.iconPrefixCls, j = n(), F = L ? "css" : "js", W = hn(function() {
        var X = /* @__PURE__ */ new Set();
        return L && Object.keys(v.unitless || {}).forEach(function(G) {
          X.add(Pe(G, L.prefix)), X.add(Pe(G, ut(w, L.prefix)));
        }), an(F, X);
      }, [F, w, L == null ? void 0 : L.prefix]), U = un(F), K = U.max, J = U.min, Z = {
        theme: P,
        token: z,
        hashId: O,
        nonce: function() {
          return j.nonce;
        },
        clientOnly: v.clientOnly,
        layer: y,
        // antd is always at top of styles
        order: v.order || -999
      };
      typeof s == "function" && Ye(D(D({}, Z), {}, {
        clientOnly: !1,
        path: ["Shared", _]
      }), function() {
        return s(z, {
          prefix: {
            rootPrefixCls: _,
            iconPrefixCls: T
          },
          csp: j
        });
      });
      var ee = Ye(D(D({}, Z), {}, {
        path: [k, C, T]
      }), function() {
        if (v.injectStyle === !1)
          return [];
        var X = cn(z), G = X.token, At = X.flush, q = ht(w, S, b), Ft = ".".concat(C), Ue = ft(w, S, q, {
          deprecatedTokens: v.deprecatedTokens
        });
        L && q && N(q) === "object" && Object.keys(q).forEach(function(Ke) {
          q[Ke] = "var(".concat(Pe(Ke, ut(w, L.prefix)), ")");
        });
        var Ge = Ne(G, {
          componentCls: Ft,
          prefixCls: C,
          iconCls: ".".concat(T),
          antCls: ".".concat(_),
          calc: W,
          // @ts-ignore
          max: K,
          // @ts-ignore
          min: J
        }, L ? q : Ue), Xt = g(Ge, {
          hashId: O,
          prefixCls: C,
          rootPrefixCls: _,
          iconPrefixCls: T
        });
        At(w, Ue);
        var Nt = typeof i == "function" ? i(Ge, C, x, v.resetFont) : null;
        return [v.resetStyle === !1 ? null : Nt, Xt];
      });
      return [ee, O];
    };
  }
  function f(d, g, b) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = u(d, g, b, D({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, v)), p = function(k) {
      var y = k.prefixCls, C = k.rootCls, x = C === void 0 ? y : C;
      return m(y, x), null;
    };
    return p;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: f,
    genComponentStyleHook: u
  };
}
const $ = Math.round;
function ke(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const mt = (e, t, n) => n === 0 ? e : e / 100;
function te(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class V {
  constructor(t) {
    R(this, "isValid", !0), R(this, "r", 0), R(this, "g", 0), R(this, "b", 0), R(this, "a", 1), R(this, "_h", void 0), R(this, "_s", void 0), R(this, "_l", void 0), R(this, "_v", void 0), R(this, "_max", void 0), R(this, "_min", void 0), R(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(s) {
        return o.startsWith(s);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof V)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = te(t.r), this.g = te(t.g), this.b = te(t.b), this.a = typeof t.a == "number" ? te(t.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(t);
    else if (n("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const n = this.toHsv();
    return n.h = t, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(s) {
      const i = s / 255;
      return i <= 0.03928 ? i / 12.92 : Math.pow((i + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), o = t(this.g), r = t(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = $(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - t / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + t / 100;
    return r > 1 && (r = 1), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const o = this._c(t), r = n / 100, s = (a) => (o[a] - this[a]) * r + this[a], i = {
      r: $(s("r")),
      g: $(s("g")),
      b: $(s("b")),
      a: $(s("a") * 100) / 100
    };
    return this._c(i);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (s) => $((this[s] * this.a + n[s] * n.a * (1 - this.a)) / o);
    return this._c({
      r: r("r"),
      g: r("g"),
      b: r("b"),
      a: o
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.g || 0).toString(16);
    t += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (t += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const s = $(this.a * 255).toString(16);
      t += s.length === 2 ? s : "0" + s;
    }
    return t;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const t = this.getHue(), n = $(this.getSaturation() * 100), o = $(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${o}%,${this.a})` : `hsl(${t},${n}%,${o}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(t, n, o) {
    const r = this.clone();
    return r[t] = te(n, o), r;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const n = t.replace("#", "");
    function o(r, s) {
      return parseInt(n[r] + n[s || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = t % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const d = $(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let s = 0, i = 0, a = 0;
    const l = t / 60, c = (1 - Math.abs(2 * o - 1)) * n, u = c * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (s = c, i = u) : l >= 1 && l < 2 ? (s = u, i = c) : l >= 2 && l < 3 ? (i = c, a = u) : l >= 3 && l < 4 ? (i = u, a = c) : l >= 4 && l < 5 ? (s = u, a = c) : l >= 5 && l < 6 && (s = c, a = u);
    const f = o - c / 2;
    this.r = $((s + f) * 255), this.g = $((i + f) * 255), this.b = $((a + f) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const s = $(o * 255);
    if (this.r = s, this.g = s, this.b = s, n <= 0)
      return;
    const i = t / 60, a = Math.floor(i), l = i - a, c = $(o * (1 - n) * 255), u = $(o * (1 - n * l) * 255), f = $(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = c;
        break;
      case 1:
        this.r = u, this.b = c;
        break;
      case 2:
        this.r = c, this.b = f;
        break;
      case 3:
        this.r = c, this.g = u;
        break;
      case 4:
        this.r = f, this.g = c;
        break;
      case 5:
      default:
        this.g = c, this.b = u;
        break;
    }
  }
  fromHsvString(t) {
    const n = ke(t, mt);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = ke(t, mt);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = ke(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? $(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const pn = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, bn = Object.assign(Object.assign({}, pn), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function je(e) {
  return e >= 0 && e <= 255;
}
function ie(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: s
  } = new V(e).toRgb();
  if (s < 1)
    return e;
  const {
    r: i,
    g: a,
    b: l
  } = new V(t).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const u = Math.round((n - i * (1 - c)) / c), f = Math.round((o - a * (1 - c)) / c), d = Math.round((r - l * (1 - c)) / c);
    if (je(u) && je(f) && je(d))
      return new V({
        r: u,
        g: f,
        b: d,
        a: Math.round(c * 100) / 100
      }).toRgbString();
  }
  return new V({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var yn = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function vn(e) {
  const {
    override: t
  } = e, n = yn(e, ["override"]), o = Object.assign({}, t);
  Object.keys(bn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), s = 480, i = 576, a = 768, l = 992, c = 1200, u = 1600;
  if (r.motion === !1) {
    const d = "0s";
    r.motionDurationFast = d, r.motionDurationMid = d, r.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: ie(r.colorBorderSecondary, r.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: r.colorTextQuaternary,
    colorTextDisabled: r.colorTextQuaternary,
    colorTextHeading: r.colorText,
    colorTextLabel: r.colorTextSecondary,
    colorTextDescription: r.colorTextTertiary,
    colorTextLightSolid: r.colorWhite,
    colorHighlight: r.colorError,
    colorBgTextHover: r.colorFillSecondary,
    colorBgTextActive: r.colorFill,
    colorIcon: r.colorTextTertiary,
    colorIconHover: r.colorText,
    colorErrorOutline: ie(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: ie(r.colorWarningBg, r.colorBgContainer),
    // Font
    fontSizeIcon: r.fontSizeSM,
    // Line
    lineWidthFocus: r.lineWidth * 3,
    // Control
    lineWidth: r.lineWidth,
    controlOutlineWidth: r.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: r.controlHeight / 2,
    controlItemBgHover: r.colorFillTertiary,
    controlItemBgActive: r.colorPrimaryBg,
    controlItemBgActiveHover: r.colorPrimaryBgHover,
    controlItemBgActiveDisabled: r.colorFill,
    controlTmpOutline: r.colorFillQuaternary,
    controlOutline: ie(r.colorPrimaryBg, r.colorBgContainer),
    lineType: r.lineType,
    borderRadius: r.borderRadius,
    borderRadiusXS: r.borderRadiusXS,
    borderRadiusSM: r.borderRadiusSM,
    borderRadiusLG: r.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: r.sizeXXS,
    paddingXS: r.sizeXS,
    paddingSM: r.sizeSM,
    padding: r.size,
    paddingMD: r.sizeMD,
    paddingLG: r.sizeLG,
    paddingXL: r.sizeXL,
    paddingContentHorizontalLG: r.sizeLG,
    paddingContentVerticalLG: r.sizeMS,
    paddingContentHorizontal: r.sizeMS,
    paddingContentVertical: r.sizeSM,
    paddingContentHorizontalSM: r.size,
    paddingContentVerticalSM: r.sizeXS,
    marginXXS: r.sizeXXS,
    marginXS: r.sizeXS,
    marginSM: r.sizeSM,
    margin: r.size,
    marginMD: r.sizeMD,
    marginLG: r.sizeLG,
    marginXL: r.sizeXL,
    marginXXL: r.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: s,
    screenXSMin: s,
    screenXSMax: i - 1,
    screenSM: i,
    screenSMMin: i,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: c - 1,
    screenXL: c,
    screenXLMin: c,
    screenXLMax: u - 1,
    screenXXL: u,
    screenXXLMin: u,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new V("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new V("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new V("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), o);
}
const xn = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, Sn = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, Cn = rr($e.defaultAlgorithm), _n = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, Ht = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...s
  } = t;
  let i = {
    ...o,
    override: r
  };
  return i = vn(i), s && Object.entries(s).forEach(([a, l]) => {
    const {
      theme: c,
      ...u
    } = l;
    let f = u;
    c && (f = Ht({
      ...i,
      ...u
    }, {
      override: u
    }, c)), i[a] = f;
  }), i;
};
function wn() {
  const {
    token: e,
    hashed: t,
    theme: n = Cn,
    override: o,
    cssVar: r
  } = h.useContext($e._internalContext), [s, i, a] = nr(n, [$e.defaultSeed, e], {
    salt: `${Xr}-${t || ""}`,
    override: o,
    getComputedToken: Ht,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: xn,
      ignore: Sn,
      preserve: _n
    }
  });
  return [n, a, t ? i : "", s, r];
}
const {
  genStyleHooks: Tn
} = mn({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = he();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = wn();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = he();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var En = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, Mn = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Pn = "".concat(En, " ").concat(Mn).split(/[\s\n]+/), On = "aria-", In = "data-";
function pt(e, t) {
  return e.indexOf(t) === 0;
}
function Rn(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = D({}, t);
  var o = {};
  return Object.keys(e).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || pt(r, On)) || // Data
    n.data && pt(r, In) || // Attr
    n.attr && Pn.includes(r)) && (o[r] = e[r]);
  }), o;
}
function ae(e) {
  return typeof e == "string";
}
const kn = (e, t, n, o) => {
  const r = I.useRef(""), [s, i] = I.useState(1), a = t && ae(e);
  return Qr(() => {
    !a && ae(e) ? i(e.length) : ae(e) && ae(r.current) && e.indexOf(r.current) !== 0 && i(1), r.current = e;
  }, [e]), I.useEffect(() => {
    if (a && s < e.length) {
      const c = setTimeout(() => {
        i((u) => u + n);
      }, o);
      return () => {
        clearTimeout(c);
      };
    }
  }, [s, t, e]), [a ? e.slice(0, s) : e, a && s < e.length];
};
function jn(e) {
  return I.useMemo(() => {
    if (!e)
      return [!1, 0, 0, null];
    let t = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof e == "object" && (t = {
      ...t,
      ...e
    }), [!0, t.step, t.interval, t.suffix];
  }, [e]);
}
const Ln = ({
  prefixCls: e
}) => /* @__PURE__ */ h.createElement("span", {
  className: `${e}-dot`
}, /* @__PURE__ */ h.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ h.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ h.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-3"
})), $n = (e) => {
  const {
    componentCls: t,
    paddingSM: n,
    padding: o
  } = e;
  return {
    [t]: {
      [`${t}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${oe(n)} ${oe(o)}`,
          borderRadius: e.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: e.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${e.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: e.boxShadowTertiary
        }
      }
    }
  };
}, Dn = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    padding: s,
    calc: i
  } = e, a = i(n).mul(o).div(2).add(r).equal(), l = `${t}-content`;
  return {
    [t]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: i(s).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: e.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: e.borderRadiusXS
      }
    }
  };
}, Hn = (e) => {
  const {
    componentCls: t,
    padding: n
  } = e;
  return {
    [`${t}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: n,
      overflowY: "auto"
    }
  };
}, Bn = new St("loadingMove", {
  "0%": {
    transform: "translateY(0)"
  },
  "10%": {
    transform: "translateY(4px)"
  },
  "20%": {
    transform: "translateY(0)"
  },
  "30%": {
    transform: "translateY(-4px)"
  },
  "40%": {
    transform: "translateY(0)"
  }
}), zn = new St("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), An = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    colorText: s,
    calc: i
  } = e;
  return {
    [t]: {
      display: "flex",
      columnGap: r,
      [`&${t}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${t}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`&${t}-typing ${t}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: zn,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${t}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${t}-header, & ${t}-footer`]: {
        fontSize: n,
        lineHeight: o,
        color: e.colorText
      },
      [`& ${t}-header`]: {
        marginBottom: e.paddingXXS
      },
      [`& ${t}-footer`]: {
        marginTop: r
      },
      // =========================== Content =============================
      [`& ${t}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${t}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: s,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        minHeight: i(r).mul(2).add(i(o).mul(n)).equal(),
        wordBreak: "break-word",
        [`& ${t}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: e.marginXS,
          padding: `0 ${oe(e.paddingXXS)}`,
          "&-item": {
            backgroundColor: e.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: Bn,
            animationDuration: "2s",
            animationIterationCount: "infinite",
            animationTimingFunction: "linear",
            "&:nth-child(1)": {
              animationDelay: "0s"
            },
            "&:nth-child(2)": {
              animationDelay: "0.2s"
            },
            "&:nth-child(3)": {
              animationDelay: "0.4s"
            }
          }
        }
      }
    }
  };
}, Fn = () => ({}), Bt = Tn("Bubble", (e) => {
  const t = Ne(e, {});
  return [An(t), Hn(t), $n(t), Dn(t)];
}, Fn), zt = /* @__PURE__ */ h.createContext({}), Xn = (e, t) => {
  const {
    prefixCls: n,
    className: o,
    rootClassName: r,
    style: s,
    classNames: i = {},
    styles: a = {},
    avatar: l,
    placement: c = "start",
    loading: u = !1,
    loadingRender: f,
    typing: d,
    content: g = "",
    messageRender: b,
    variant: v = "filled",
    shape: m,
    onTypingComplete: p,
    header: w,
    footer: k,
    ...y
  } = e, {
    onUpdate: C
  } = h.useContext(zt), x = h.useRef(null);
  h.useImperativeHandle(t, () => ({
    nativeElement: x.current
  }));
  const {
    direction: M,
    getPrefixCls: P
  } = he(), S = P("bubble", n), O = Wr("bubble"), [z, L, A, _] = jn(d), [T, j] = kn(g, z, L, A);
  h.useEffect(() => {
    C == null || C();
  }, [T]);
  const F = h.useRef(!1);
  h.useEffect(() => {
    !j && !u ? F.current || (F.current = !0, p == null || p()) : F.current = !1;
  }, [j, u]);
  const [W, U, K] = Bt(S), J = Y(S, r, O.className, o, U, K, `${S}-${c}`, {
    [`${S}-rtl`]: M === "rtl",
    [`${S}-typing`]: j && !u && !b && !_
  }), Z = /* @__PURE__ */ h.isValidElement(l) ? l : /* @__PURE__ */ h.createElement(er, l), ee = b ? b(T) : T;
  let X;
  u ? X = f ? f() : /* @__PURE__ */ h.createElement(Ln, {
    prefixCls: S
  }) : X = /* @__PURE__ */ h.createElement(h.Fragment, null, ee, j && _);
  let G = /* @__PURE__ */ h.createElement("div", {
    style: {
      ...O.styles.content,
      ...a.content
    },
    className: Y(`${S}-content`, `${S}-content-${v}`, m && `${S}-content-${m}`, O.classNames.content, i.content)
  }, X);
  return (w || k) && (G = /* @__PURE__ */ h.createElement("div", {
    className: `${S}-content-wrapper`
  }, w && /* @__PURE__ */ h.createElement("div", {
    className: Y(`${S}-header`, O.classNames.header, i.header),
    style: {
      ...O.styles.header,
      ...a.header
    }
  }, w), G, k && /* @__PURE__ */ h.createElement("div", {
    className: Y(`${S}-footer`, O.classNames.footer, i.footer),
    style: {
      ...O.styles.footer,
      ...a.footer
    }
  }, k))), W(/* @__PURE__ */ h.createElement("div", se({
    style: {
      ...O.style,
      ...s
    },
    className: J
  }, y, {
    ref: x
  }), l && /* @__PURE__ */ h.createElement("div", {
    style: {
      ...O.styles.avatar,
      ...a.avatar
    },
    className: Y(`${S}-avatar`, O.classNames.avatar, i.avatar)
  }, Z), G));
}, Ve = /* @__PURE__ */ h.forwardRef(Xn);
function Nn(e) {
  const [t, n] = h.useState(e.length), o = h.useMemo(() => e.slice(0, t), [e, t]), r = h.useMemo(() => {
    const i = o[o.length - 1];
    return i ? i.key : null;
  }, [o]);
  h.useEffect(() => {
    var i;
    if (!(o.length && o.every((a, l) => {
      var c;
      return a.key === ((c = e[l]) == null ? void 0 : c.key);
    }))) {
      if (o.length === 0)
        n(1);
      else
        for (let a = 0; a < o.length; a += 1)
          if (o[a].key !== ((i = e[a]) == null ? void 0 : i.key)) {
            n(a);
            break;
          }
    }
  }, [e]);
  const s = Pt((i) => {
    i === r && n(t + 1);
  });
  return [o, s];
}
function Vn(e, t) {
  const n = I.useCallback((o, r) => typeof t == "function" ? t(o, r) : t ? t[o.role] || {} : {}, [t]);
  return I.useMemo(() => (e || []).map((o, r) => {
    const s = o.key ?? `preset_${r}`;
    return {
      ...n(o, r),
      ...o,
      key: s
    };
  }), [e, n]);
}
const Wn = 1, Un = (e, t) => {
  const {
    prefixCls: n,
    rootClassName: o,
    className: r,
    items: s,
    autoScroll: i = !0,
    roles: a,
    ...l
  } = e, c = Rn(l, {
    attr: !0,
    aria: !0
  }), u = I.useRef(null), f = I.useRef({}), {
    getPrefixCls: d
  } = he(), g = d("bubble", n), b = `${g}-list`, [v, m, p] = Bt(g), [w, k] = I.useState(!1);
  I.useEffect(() => (k(!0), () => {
    k(!1);
  }), []);
  const y = Vn(s, a), [C, x] = Nn(y), [M, P] = I.useState(!0), [S, O] = I.useState(0), z = (_) => {
    const T = _.target;
    P(T.scrollHeight - Math.abs(T.scrollTop) - T.clientHeight <= Wn);
  };
  I.useEffect(() => {
    i && u.current && M && u.current.scrollTo({
      top: u.current.scrollHeight
    });
  }, [S]), I.useEffect(() => {
    var _;
    if (i) {
      const T = (_ = C[C.length - 2]) == null ? void 0 : _.key, j = f.current[T];
      if (j) {
        const {
          nativeElement: F
        } = j, {
          top: W,
          bottom: U
        } = F.getBoundingClientRect(), {
          top: K,
          bottom: J
        } = u.current.getBoundingClientRect();
        W < J && U > K && (O((ee) => ee + 1), P(!0));
      }
    }
  }, [C.length]), I.useImperativeHandle(t, () => ({
    nativeElement: u.current,
    scrollTo: ({
      key: _,
      offset: T,
      behavior: j = "smooth",
      block: F
    }) => {
      if (typeof T == "number")
        u.current.scrollTo({
          top: T,
          behavior: j
        });
      else if (_ !== void 0) {
        const W = f.current[_];
        if (W) {
          const U = C.findIndex((K) => K.key === _);
          P(U === C.length - 1), W.nativeElement.scrollIntoView({
            behavior: j,
            block: F
          });
        }
      }
    }
  }));
  const L = Pt(() => {
    i && O((_) => _ + 1);
  }), A = I.useMemo(() => ({
    onUpdate: L
  }), []);
  return v(/* @__PURE__ */ I.createElement(zt.Provider, {
    value: A
  }, /* @__PURE__ */ I.createElement("div", se({}, c, {
    className: Y(b, o, r, m, p, {
      [`${b}-reach-end`]: M
    }),
    ref: u,
    onScroll: z
  }), C.map(({
    key: _,
    ...T
  }) => /* @__PURE__ */ I.createElement(Ve, se({}, T, {
    key: _,
    ref: (j) => {
      j ? f.current[_] = j : delete f.current[_];
    },
    typing: w ? T.typing : !1,
    onTypingComplete: () => {
      var j;
      (j = T.onTypingComplete) == null || j.call(T), x(_);
    }
  }))))));
}, Gn = /* @__PURE__ */ I.forwardRef(Un);
Ve.List = Gn;
const Kn = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function qn(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = Yn(n, o), t;
  }, {}) : {};
}
function Yn(e, t) {
  return typeof t == "number" && !Kn.includes(e) ? t + "px" : t;
}
function ze(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = h.Children.toArray(e._reactElement.props.children).map((s) => {
      if (h.isValidElement(s) && s.props.__slot__) {
        const {
          portals: i,
          clonedElement: a
        } = ze(s.props.el);
        return h.cloneElement(s, {
          ...s.props,
          el: a,
          children: [...h.Children.toArray(s.props.children), ...i]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(Le(h.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: i,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, i, l);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const s = o[r];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = ze(s);
      t.push(...a), n.appendChild(i);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Qn(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const bt = Wt(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, s) => {
  const i = vt(), [a, l] = Ut([]), {
    forceClone: c
  } = Jt(), u = c ? !0 : t;
  return Gt(() => {
    var v;
    if (!i.current || !e)
      return;
    let f = e;
    function d() {
      let m = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (m = f.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Qn(s, m), n && m.classList.add(...n.split(" ")), o) {
        const p = qn(o);
        Object.keys(p).forEach((w) => {
          m.style[w] = p[w];
        });
      }
    }
    let g = null, b = null;
    if (u && window.MutationObserver) {
      let m = function() {
        var y, C, x;
        (y = i.current) != null && y.contains(f) && ((C = i.current) == null || C.removeChild(f));
        const {
          portals: w,
          clonedElement: k
        } = ze(e);
        f = k, l(w), f.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (x = i.current) == null || x.appendChild(f);
      };
      m();
      const p = mr(() => {
        m(), g == null || g.disconnect(), g == null || g.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      g = new window.MutationObserver(p), g.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (v = i.current) == null || v.appendChild(f);
    return () => {
      var m, p;
      f.style.display = "", (m = i.current) != null && m.contains(f) && ((p = i.current) == null || p.removeChild(f)), g == null || g.disconnect();
    };
  }, [e, u, n, o, s, r, c]), h.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...a);
});
function yt(e) {
  const t = vt(e);
  return t.current = e, Kt((...n) => {
    var o;
    return (o = t.current) == null ? void 0 : o.call(t, ...n);
  }, []);
}
const Jn = ({
  children: e,
  ...t
}) => /* @__PURE__ */ H.jsx(H.Fragment, {
  children: e(t)
});
function Zn(e) {
  return h.createElement(Jn, {
    children: e
  });
}
function We(e, t, n) {
  const o = e.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, s) => {
      var c;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const i = {
        ...r.props,
        key: ((c = r.props) == null ? void 0 : c.key) ?? (n ? `${n}-${s}` : `${s}`)
      };
      let a = i;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((p, w) => {
          a[p] || (a[p] = {}), w !== f.length - 1 && (a = i[p]);
        });
        const d = r.slots[u];
        let g, b, v = (t == null ? void 0 : t.clone) ?? !1, m = t == null ? void 0 : t.forceClone;
        d instanceof Element ? g = d : (g = d.el, b = d.callback, v = d.clone ?? v, m = d.forceClone ?? m), m = m ?? !!b, a[f[f.length - 1]] = g ? b ? (...p) => (b(f[f.length - 1], p), /* @__PURE__ */ H.jsx(qe, {
          ...r.ctx,
          params: p,
          forceClone: m,
          children: /* @__PURE__ */ H.jsx(bt, {
            slot: g,
            clone: v
          })
        })) : Zn((p) => /* @__PURE__ */ H.jsx(qe, {
          ...r.ctx,
          forceClone: m,
          children: /* @__PURE__ */ H.jsx(bt, {
            ...p,
            slot: g,
            clone: v
          })
        })) : a[f[f.length - 1]], a = i;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return r[l] ? i[l] = We(r[l], t, `${s}`) : t != null && t.children && (i[l] = void 0, Reflect.deleteProperty(i, l)), i;
    });
}
const {
  useItems: eo,
  withItemsContextProvider: to,
  ItemHandler: go
} = xt("antdx-bubble.list-items"), {
  useItems: ro,
  withItemsContextProvider: no,
  ItemHandler: mo
} = xt("antdx-bubble.list-roles");
function oo(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function so(e, t = !1) {
  try {
    if (Ae(e))
      return e;
    if (t && !oo(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function io(e, t) {
  return de(() => so(e, t), [e, t]);
}
function ao(e, t) {
  return t((o, r) => Ae(o) ? r ? (...s) => o(...s, ...e) : o(...e) : o);
}
const lo = Symbol();
function co(e, t) {
  return ao(t, (n) => {
    var o, r;
    return {
      ...e,
      avatar: Ae(e.avatar) ? n(e.avatar) : ne(e.avatar) ? {
        ...e.avatar,
        icon: n((o = e.avatar) == null ? void 0 : o.icon),
        src: n((r = e.avatar) == null ? void 0 : r.src)
      } : e.avatar,
      footer: n(e.footer),
      header: n(e.header),
      loadingRender: n(e.loadingRender, !0),
      messageRender: n(e.messageRender, !0)
    };
  });
}
function uo({
  roles: e,
  preProcess: t,
  postProcess: n
}, o = []) {
  const r = io(e), s = yt(t), i = yt(n), {
    items: {
      roles: a
    }
  } = ro(), l = de(() => {
    var u;
    return e || ((u = We(a, {
      clone: !0,
      forceClone: !0
    })) == null ? void 0 : u.reduce((f, d) => (d.role !== void 0 && (f[d.role] = d), f), {}));
  }, [a, e]), c = de(() => (u, f) => {
    const d = f ?? u[lo], g = s(u, d) || u;
    if (g.role && (l || {})[g.role])
      return co((l || {})[g.role], [g, d]);
    let b;
    return b = i(g, d), b || {
      messageRender(v) {
        return /* @__PURE__ */ H.jsx(H.Fragment, {
          children: ne(v) ? JSON.stringify(v) : v
        });
      }
    };
  }, [l, i, s, ...o]);
  return r || c;
}
const po = Fr(no(["roles"], to(["items", "default"], ({
  items: e,
  roles: t,
  children: n,
  ...o
}) => {
  const {
    items: r
  } = eo(), s = uo({
    roles: t
  }), i = r.items.length > 0 ? r.items : r.default;
  return /* @__PURE__ */ H.jsxs(H.Fragment, {
    children: [/* @__PURE__ */ H.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ H.jsx(Ve.List, {
      ...o,
      items: de(() => e || We(i), [e, i]),
      roles: s
    })]
  });
})));
export {
  po as BubbleList,
  po as default
};
