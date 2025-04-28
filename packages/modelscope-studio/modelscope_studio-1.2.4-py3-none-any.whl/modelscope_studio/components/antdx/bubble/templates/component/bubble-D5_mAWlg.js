import { i as Ut, a as de, r as Gt, w as le, g as Kt, c as Q, b as qt } from "./Index-CMD1WPBM.js";
const R = window.ms_globals.React, d = window.ms_globals.React, Ft = window.ms_globals.React.forwardRef, Xt = window.ms_globals.React.useRef, Nt = window.ms_globals.React.useState, Vt = window.ms_globals.React.useEffect, Wt = window.ms_globals.React.version, yt = window.ms_globals.React.useMemo, Le = window.ms_globals.ReactDOM.createPortal, Yt = window.ms_globals.internalContext.useContextPropsContext, Qt = window.ms_globals.internalContext.ContextPropsProvider, Jt = window.ms_globals.antd.ConfigProvider, $e = window.ms_globals.antd.theme, Zt = window.ms_globals.antd.Avatar, oe = window.ms_globals.antdCssinjs.unit, Pe = window.ms_globals.antdCssinjs.token2CSSVar, Ge = window.ms_globals.antdCssinjs.useStyleRegister, er = window.ms_globals.antdCssinjs.useCSSVarRegister, tr = window.ms_globals.antdCssinjs.createTheme, rr = window.ms_globals.antdCssinjs.useCacheToken, bt = window.ms_globals.antdCssinjs.Keyframes;
var nr = /\s/;
function or(t) {
  for (var e = t.length; e-- && nr.test(t.charAt(e)); )
    ;
  return e;
}
var ir = /^\s+/;
function sr(t) {
  return t && t.slice(0, or(t) + 1).replace(ir, "");
}
var Ke = NaN, ar = /^[-+]0x[0-9a-f]+$/i, lr = /^0b[01]+$/i, cr = /^0o[0-7]+$/i, ur = parseInt;
function qe(t) {
  if (typeof t == "number")
    return t;
  if (Ut(t))
    return Ke;
  if (de(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = de(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = sr(t);
  var n = lr.test(t);
  return n || cr.test(t) ? ur(t.slice(2), n ? 2 : 8) : ar.test(t) ? Ke : +t;
}
var Oe = function() {
  return Gt.Date.now();
}, fr = "Expected a function", dr = Math.max, hr = Math.min;
function gr(t, e, n) {
  var o, r, i, s, a, l, c = 0, u = !1, f = !1, h = !0;
  if (typeof t != "function")
    throw new TypeError(fr);
  e = qe(e) || 0, de(n) && (u = !!n.leading, f = "maxWait" in n, i = f ? dr(qe(n.maxWait) || 0, e) : i, h = "trailing" in n ? !!n.trailing : h);
  function S(p) {
    var M = o, P = r;
    return o = r = void 0, c = p, s = t.apply(P, M), s;
  }
  function C(p) {
    return c = p, a = setTimeout(x, e), u ? S(p) : s;
  }
  function E(p) {
    var M = p - l, P = p - c, y = e - M;
    return f ? hr(y, i - P) : y;
  }
  function m(p) {
    var M = p - l, P = p - c;
    return l === void 0 || M >= e || M < 0 || f && P >= i;
  }
  function x() {
    var p = Oe();
    if (m(p))
      return w(p);
    a = setTimeout(x, E(p));
  }
  function w(p) {
    return a = void 0, h && o ? S(p) : (o = r = void 0, s);
  }
  function j() {
    a !== void 0 && clearTimeout(a), c = 0, o = l = r = a = void 0;
  }
  function g() {
    return a === void 0 ? s : w(Oe());
  }
  function b() {
    var p = Oe(), M = m(p);
    if (o = arguments, r = this, l = p, M) {
      if (a === void 0)
        return C(l);
      if (f)
        return clearTimeout(a), a = setTimeout(x, e), S(l);
    }
    return a === void 0 && (a = setTimeout(x, e)), s;
  }
  return b.cancel = j, b.flush = g, b;
}
var vt = {
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
var mr = d, pr = Symbol.for("react.element"), yr = Symbol.for("react.fragment"), br = Object.prototype.hasOwnProperty, vr = mr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Sr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function St(t, e, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), e.key !== void 0 && (i = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) br.call(e, o) && !Sr.hasOwnProperty(o) && (r[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) r[o] === void 0 && (r[o] = e[o]);
  return {
    $$typeof: pr,
    type: t,
    key: i,
    ref: s,
    props: r,
    _owner: vr.current
  };
}
me.Fragment = yr;
me.jsx = St;
me.jsxs = St;
vt.exports = me;
var D = vt.exports;
const {
  SvelteComponent: xr,
  assign: Ye,
  binding_callbacks: Qe,
  check_outros: Cr,
  children: xt,
  claim_element: Ct,
  claim_space: _r,
  component_subscribe: Je,
  compute_slots: wr,
  create_slot: Tr,
  detach: J,
  element: _t,
  empty: Ze,
  exclude_internal_props: et,
  get_all_dirty_from_scope: Er,
  get_slot_changes: Mr,
  group_outros: Pr,
  init: Or,
  insert_hydration: ce,
  safe_not_equal: Rr,
  set_custom_element_data: wt,
  space: Ir,
  transition_in: ue,
  transition_out: De,
  update_slot_base: jr
} = window.__gradio__svelte__internal, {
  beforeUpdate: kr,
  getContext: Lr,
  onDestroy: $r,
  setContext: Dr
} = window.__gradio__svelte__internal;
function tt(t) {
  let e, n;
  const o = (
    /*#slots*/
    t[7].default
  ), r = Tr(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = _t("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      e = Ct(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = xt(e);
      r && r.l(s), s.forEach(J), this.h();
    },
    h() {
      wt(e, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      ce(i, e, s), r && r.m(e, null), t[9](e), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && jr(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? Mr(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Er(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (ue(r, i), n = !0);
    },
    o(i) {
      De(r, i), n = !1;
    },
    d(i) {
      i && J(e), r && r.d(i), t[9](null);
    }
  };
}
function Br(t) {
  let e, n, o, r, i = (
    /*$$slots*/
    t[4].default && tt(t)
  );
  return {
    c() {
      e = _t("react-portal-target"), n = Ir(), i && i.c(), o = Ze(), this.h();
    },
    l(s) {
      e = Ct(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), xt(e).forEach(J), n = _r(s), i && i.l(s), o = Ze(), this.h();
    },
    h() {
      wt(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      ce(s, e, a), t[8](e), ce(s, n, a), i && i.m(s, a), ce(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && ue(i, 1)) : (i = tt(s), i.c(), ue(i, 1), i.m(o.parentNode, o)) : i && (Pr(), De(i, 1, 1, () => {
        i = null;
      }), Cr());
    },
    i(s) {
      r || (ue(i), r = !0);
    },
    o(s) {
      De(i), r = !1;
    },
    d(s) {
      s && (J(e), J(n), J(o)), t[8](null), i && i.d(s);
    }
  };
}
function rt(t) {
  const {
    svelteInit: e,
    ...n
  } = t;
  return n;
}
function Hr(t, e, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = e;
  const a = wr(i);
  let {
    svelteInit: l
  } = e;
  const c = le(rt(e)), u = le();
  Je(t, u, (g) => n(0, o = g));
  const f = le();
  Je(t, f, (g) => n(1, r = g));
  const h = [], S = Lr("$$ms-gr-react-wrapper"), {
    slotKey: C,
    slotIndex: E,
    subSlotIndex: m
  } = Kt() || {}, x = l({
    parent: S,
    props: c,
    target: u,
    slot: f,
    slotKey: C,
    slotIndex: E,
    subSlotIndex: m,
    onDestroy(g) {
      h.push(g);
    }
  });
  Dr("$$ms-gr-react-wrapper", x), kr(() => {
    c.set(rt(e));
  }), $r(() => {
    h.forEach((g) => g());
  });
  function w(g) {
    Qe[g ? "unshift" : "push"](() => {
      o = g, u.set(o);
    });
  }
  function j(g) {
    Qe[g ? "unshift" : "push"](() => {
      r = g, f.set(r);
    });
  }
  return t.$$set = (g) => {
    n(17, e = Ye(Ye({}, e), et(g))), "svelteInit" in g && n(5, l = g.svelteInit), "$$scope" in g && n(6, s = g.$$scope);
  }, e = et(e), [o, r, u, f, a, l, s, i, w, j];
}
class zr extends xr {
  constructor(e) {
    super(), Or(this, e, Hr, Br, Rr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ro
} = window.__gradio__svelte__internal, nt = window.ms_globals.rerender, Re = window.ms_globals.tree;
function Ar(t, e = {}) {
  function n(o) {
    const r = le(), i = new zr({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, l = s.parent ?? Re;
          return l.nodes = [...l.nodes, a], nt({
            createPortal: Le,
            node: Re
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== r), nt({
              createPortal: Le,
              node: Re
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(i), i;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Fr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Xr(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const o = t[n];
    return e[n] = Nr(n, o), e;
  }, {}) : {};
}
function Nr(t, e) {
  return typeof e == "number" && !Fr.includes(t) ? e + "px" : e;
}
function Be(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement) {
    const r = d.Children.toArray(t._reactElement.props.children).map((i) => {
      if (d.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Be(i.props.el);
        return d.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...d.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = t._reactElement.props.children, e.push(Le(d.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, s, l);
    });
  });
  const o = Array.from(t.childNodes);
  for (let r = 0; r < o.length; r++) {
    const i = o[r];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Be(i);
      e.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function Vr(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const K = Ft(({
  slot: t,
  clone: e,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = Xt(), [a, l] = Nt([]), {
    forceClone: c
  } = Yt(), u = c ? !0 : e;
  return Vt(() => {
    var E;
    if (!s.current || !t)
      return;
    let f = t;
    function h() {
      let m = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (m = f.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Vr(i, m), n && m.classList.add(...n.split(" ")), o) {
        const x = Xr(o);
        Object.keys(x).forEach((w) => {
          m.style[w] = x[w];
        });
      }
    }
    let S = null, C = null;
    if (u && window.MutationObserver) {
      let m = function() {
        var g, b, p;
        (g = s.current) != null && g.contains(f) && ((b = s.current) == null || b.removeChild(f));
        const {
          portals: w,
          clonedElement: j
        } = Be(t);
        f = j, l(w), f.style.display = "contents", C && clearTimeout(C), C = setTimeout(() => {
          h();
        }, 50), (p = s.current) == null || p.appendChild(f);
      };
      m();
      const x = gr(() => {
        m(), S == null || S.disconnect(), S == null || S.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      S = new window.MutationObserver(x), S.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", h(), (E = s.current) == null || E.appendChild(f);
    return () => {
      var m, x;
      f.style.display = "", (m = s.current) != null && m.contains(f) && ((x = s.current) == null || x.removeChild(f)), S == null || S.disconnect();
    };
  }, [t, u, n, o, i, r, c]), d.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Wr = "1.1.0", Ur = /* @__PURE__ */ d.createContext({}), Gr = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Kr = (t) => {
  const e = d.useContext(Ur);
  return d.useMemo(() => ({
    ...Gr,
    ...e[t]
  }), [e[t]]);
};
function ie() {
  return ie = Object.assign ? Object.assign.bind() : function(t) {
    for (var e = 1; e < arguments.length; e++) {
      var n = arguments[e];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (t[o] = n[o]);
    }
    return t;
  }, ie.apply(null, arguments);
}
function he() {
  const {
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = d.useContext(Jt.ConfigContext);
  return {
    theme: r,
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o
  };
}
function Tt(t) {
  var e = R.useRef();
  e.current = t;
  var n = R.useCallback(function() {
    for (var o, r = arguments.length, i = new Array(r), s = 0; s < r; s++)
      i[s] = arguments[s];
    return (o = e.current) === null || o === void 0 ? void 0 : o.call.apply(o, [e].concat(i));
  }, []);
  return n;
}
function qr(t) {
  if (Array.isArray(t)) return t;
}
function Yr(t, e) {
  var n = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], l = !0, c = !1;
    try {
      if (i = (n = n.call(t)).next, e === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = i.call(n)).done) && (a.push(o.value), a.length !== e); l = !0) ;
    } catch (u) {
      c = !0, r = u;
    } finally {
      try {
        if (!l && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (c) throw r;
      }
    }
    return a;
  }
}
function ot(t, e) {
  (e == null || e > t.length) && (e = t.length);
  for (var n = 0, o = Array(e); n < e; n++) o[n] = t[n];
  return o;
}
function Qr(t, e) {
  if (t) {
    if (typeof t == "string") return ot(t, e);
    var n = {}.toString.call(t).slice(8, -1);
    return n === "Object" && t.constructor && (n = t.constructor.name), n === "Map" || n === "Set" ? Array.from(t) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? ot(t, e) : void 0;
  }
}
function Jr() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function fe(t, e) {
  return qr(t) || Yr(t, e) || Qr(t, e) || Jr();
}
function Zr() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var it = Zr() ? R.useLayoutEffect : R.useEffect, en = function(e, n) {
  var o = R.useRef(!0);
  it(function() {
    return e(o.current);
  }, n), it(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
};
function N(t) {
  "@babel/helpers - typeof";
  return N = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, N(t);
}
var T = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ae = Symbol.for("react.element"), Fe = Symbol.for("react.portal"), pe = Symbol.for("react.fragment"), ye = Symbol.for("react.strict_mode"), be = Symbol.for("react.profiler"), ve = Symbol.for("react.provider"), Se = Symbol.for("react.context"), tn = Symbol.for("react.server_context"), xe = Symbol.for("react.forward_ref"), Ce = Symbol.for("react.suspense"), _e = Symbol.for("react.suspense_list"), we = Symbol.for("react.memo"), Te = Symbol.for("react.lazy"), rn = Symbol.for("react.offscreen"), Et;
Et = Symbol.for("react.module.reference");
function H(t) {
  if (typeof t == "object" && t !== null) {
    var e = t.$$typeof;
    switch (e) {
      case Ae:
        switch (t = t.type, t) {
          case pe:
          case be:
          case ye:
          case Ce:
          case _e:
            return t;
          default:
            switch (t = t && t.$$typeof, t) {
              case tn:
              case Se:
              case xe:
              case Te:
              case we:
              case ve:
                return t;
              default:
                return e;
            }
        }
      case Fe:
        return e;
    }
  }
}
T.ContextConsumer = Se;
T.ContextProvider = ve;
T.Element = Ae;
T.ForwardRef = xe;
T.Fragment = pe;
T.Lazy = Te;
T.Memo = we;
T.Portal = Fe;
T.Profiler = be;
T.StrictMode = ye;
T.Suspense = Ce;
T.SuspenseList = _e;
T.isAsyncMode = function() {
  return !1;
};
T.isConcurrentMode = function() {
  return !1;
};
T.isContextConsumer = function(t) {
  return H(t) === Se;
};
T.isContextProvider = function(t) {
  return H(t) === ve;
};
T.isElement = function(t) {
  return typeof t == "object" && t !== null && t.$$typeof === Ae;
};
T.isForwardRef = function(t) {
  return H(t) === xe;
};
T.isFragment = function(t) {
  return H(t) === pe;
};
T.isLazy = function(t) {
  return H(t) === Te;
};
T.isMemo = function(t) {
  return H(t) === we;
};
T.isPortal = function(t) {
  return H(t) === Fe;
};
T.isProfiler = function(t) {
  return H(t) === be;
};
T.isStrictMode = function(t) {
  return H(t) === ye;
};
T.isSuspense = function(t) {
  return H(t) === Ce;
};
T.isSuspenseList = function(t) {
  return H(t) === _e;
};
T.isValidElementType = function(t) {
  return typeof t == "string" || typeof t == "function" || t === pe || t === be || t === ye || t === Ce || t === _e || t === rn || typeof t == "object" && t !== null && (t.$$typeof === Te || t.$$typeof === we || t.$$typeof === ve || t.$$typeof === Se || t.$$typeof === xe || t.$$typeof === Et || t.getModuleId !== void 0);
};
T.typeOf = H;
Number(Wt.split(".")[0]);
function nn(t, e) {
  if (N(t) != "object" || !t) return t;
  var n = t[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(t, e);
    if (N(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function Mt(t) {
  var e = nn(t, "string");
  return N(e) == "symbol" ? e : e + "";
}
function I(t, e, n) {
  return (e = Mt(e)) in t ? Object.defineProperty(t, e, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = n, t;
}
function st(t, e) {
  var n = Object.keys(t);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(t);
    e && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(t, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function B(t) {
  for (var e = 1; e < arguments.length; e++) {
    var n = arguments[e] != null ? arguments[e] : {};
    e % 2 ? st(Object(n), !0).forEach(function(o) {
      I(t, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : st(Object(n)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return t;
}
function Ee(t, e) {
  if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function on(t, e) {
  for (var n = 0; n < e.length; n++) {
    var o = e[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, Mt(o.key), o);
  }
}
function Me(t, e, n) {
  return e && on(t.prototype, e), Object.defineProperty(t, "prototype", {
    writable: !1
  }), t;
}
function He(t, e) {
  return He = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, He(t, e);
}
function Pt(t, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  t.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: t,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(t, "prototype", {
    writable: !1
  }), e && He(t, e);
}
function ge(t) {
  return ge = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, ge(t);
}
function Ot() {
  try {
    var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Ot = function() {
    return !!t;
  })();
}
function ne(t) {
  if (t === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return t;
}
function sn(t, e) {
  if (e && (N(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ne(t);
}
function Rt(t) {
  var e = Ot();
  return function() {
    var n, o = ge(t);
    if (e) {
      var r = ge(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return sn(this, n);
  };
}
var It = /* @__PURE__ */ Me(function t() {
  Ee(this, t);
}), jt = "CALC_UNIT", an = new RegExp(jt, "g");
function Ie(t) {
  return typeof t == "number" ? "".concat(t).concat(jt) : t;
}
var ln = /* @__PURE__ */ function(t) {
  Pt(n, t);
  var e = Rt(n);
  function n(o, r) {
    var i;
    Ee(this, n), i = e.call(this), I(ne(i), "result", ""), I(ne(i), "unitlessCssVar", void 0), I(ne(i), "lowPriority", void 0);
    var s = N(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = Ie(o) : s === "string" && (i.result = o), i;
  }
  return Me(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(Ie(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(Ie(r))), this.lowPriority = !0, this;
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
      var i = this, s = r || {}, a = s.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(c) {
        return i.result.includes(c);
      }) && (l = !1), this.result = this.result.replace(an, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(It), cn = /* @__PURE__ */ function(t) {
  Pt(n, t);
  var e = Rt(n);
  function n(o) {
    var r;
    return Ee(this, n), r = e.call(this), I(ne(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
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
}(It), un = function(e, n) {
  var o = e === "css" ? ln : cn;
  return function(r) {
    return new o(r, n);
  };
}, at = function(e, n) {
  return "".concat([n, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function lt(t, e, n, o) {
  var r = B({}, e[t]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var l = fe(a, 2), c = l[0], u = l[1];
      if (r != null && r[c] || r != null && r[u]) {
        var f;
        (f = r[u]) !== null && f !== void 0 || (r[u] = r == null ? void 0 : r[c]);
      }
    });
  }
  var s = B(B({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var kt = typeof CSSINJS_STATISTIC < "u", ze = !0;
function Xe() {
  for (var t = arguments.length, e = new Array(t), n = 0; n < t; n++)
    e[n] = arguments[n];
  if (!kt)
    return Object.assign.apply(Object, [{}].concat(e));
  ze = !1;
  var o = {};
  return e.forEach(function(r) {
    if (N(r) === "object") {
      var i = Object.keys(r);
      i.forEach(function(s) {
        Object.defineProperty(o, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[s];
          }
        });
      });
    }
  }), ze = !0, o;
}
var ct = {};
function fn() {
}
var dn = function(e) {
  var n, o = e, r = fn;
  return kt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(e, {
    get: function(s, a) {
      if (ze) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var l;
    ct[s] = {
      global: Array.from(n),
      component: B(B({}, (l = ct[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function ut(t, e, n) {
  if (typeof n == "function") {
    var o;
    return n(Xe(e, (o = e[t]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function hn(t) {
  return t === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(i) {
        return oe(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(i) {
        return oe(i);
      }).join(","), ")");
    }
  };
}
var gn = 1e3 * 60 * 10, mn = /* @__PURE__ */ function() {
  function t() {
    Ee(this, t), I(this, "map", /* @__PURE__ */ new Map()), I(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), I(this, "nextID", 0), I(this, "lastAccessBeat", /* @__PURE__ */ new Map()), I(this, "accessBeat", 0);
  }
  return Me(t, [{
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
      var o = this, r = n.map(function(i) {
        return i && N(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(N(i), "_").concat(i);
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
        this.lastAccessBeat.forEach(function(r, i) {
          o - r > gn && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), t;
}(), ft = new mn();
function pn(t, e) {
  return d.useMemo(function() {
    var n = ft.get(e);
    if (n)
      return n;
    var o = t();
    return ft.set(e, o), o;
  }, e);
}
var yn = function() {
  return {};
};
function bn(t) {
  var e = t.useCSP, n = e === void 0 ? yn : e, o = t.useToken, r = t.usePrefix, i = t.getResetStyles, s = t.getCommonStyle, a = t.getCompUnitless;
  function l(h, S, C, E) {
    var m = Array.isArray(h) ? h[0] : h;
    function x(P) {
      return "".concat(String(m)).concat(P.slice(0, 1).toUpperCase()).concat(P.slice(1));
    }
    var w = (E == null ? void 0 : E.unitless) || {}, j = typeof a == "function" ? a(h) : {}, g = B(B({}, j), {}, I({}, x("zIndexPopup"), !0));
    Object.keys(w).forEach(function(P) {
      g[x(P)] = w[P];
    });
    var b = B(B({}, E), {}, {
      unitless: g,
      prefixToken: x
    }), p = u(h, S, C, b), M = c(m, C, b);
    return function(P) {
      var y = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : P, O = p(P, y), z = fe(O, 2), L = z[1], A = M(y), v = fe(A, 2), _ = v[0], k = v[1];
      return [_, L, k];
    };
  }
  function c(h, S, C) {
    var E = C.unitless, m = C.injectStyle, x = m === void 0 ? !0 : m, w = C.prefixToken, j = C.ignore, g = function(M) {
      var P = M.rootCls, y = M.cssVar, O = y === void 0 ? {} : y, z = o(), L = z.realToken;
      return er({
        path: [h],
        prefix: O.prefix,
        key: O.key,
        unitless: E,
        ignore: j,
        token: L,
        scope: P
      }, function() {
        var A = ut(h, L, S), v = lt(h, L, A, {
          deprecatedTokens: C == null ? void 0 : C.deprecatedTokens
        });
        return Object.keys(A).forEach(function(_) {
          v[w(_)] = v[_], delete v[_];
        }), v;
      }), null;
    }, b = function(M) {
      var P = o(), y = P.cssVar;
      return [function(O) {
        return x && y ? /* @__PURE__ */ d.createElement(d.Fragment, null, /* @__PURE__ */ d.createElement(g, {
          rootCls: M,
          cssVar: y,
          component: h
        }), O) : O;
      }, y == null ? void 0 : y.key];
    };
    return b;
  }
  function u(h, S, C) {
    var E = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(h) ? h : [h, h], x = fe(m, 1), w = x[0], j = m.join("-"), g = t.layer || {
      name: "antd"
    };
    return function(b) {
      var p = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : b, M = o(), P = M.theme, y = M.realToken, O = M.hashId, z = M.token, L = M.cssVar, A = r(), v = A.rootPrefixCls, _ = A.iconPrefixCls, k = n(), F = L ? "css" : "js", W = pn(function() {
        var X = /* @__PURE__ */ new Set();
        return L && Object.keys(E.unitless || {}).forEach(function(G) {
          X.add(Pe(G, L.prefix)), X.add(Pe(G, at(w, L.prefix)));
        }), un(F, X);
      }, [F, w, L == null ? void 0 : L.prefix]), U = hn(F), q = U.max, Z = U.min, ee = {
        theme: P,
        token: z,
        hashId: O,
        nonce: function() {
          return k.nonce;
        },
        clientOnly: E.clientOnly,
        layer: g,
        // antd is always at top of styles
        order: E.order || -999
      };
      typeof i == "function" && Ge(B(B({}, ee), {}, {
        clientOnly: !1,
        path: ["Shared", v]
      }), function() {
        return i(z, {
          prefix: {
            rootPrefixCls: v,
            iconPrefixCls: _
          },
          csp: k
        });
      });
      var te = Ge(B(B({}, ee), {}, {
        path: [j, b, _]
      }), function() {
        if (E.injectStyle === !1)
          return [];
        var X = dn(z), G = X.token, Bt = X.flush, Y = ut(w, y, C), Ht = ".".concat(b), Ve = lt(w, y, Y, {
          deprecatedTokens: E.deprecatedTokens
        });
        L && Y && N(Y) === "object" && Object.keys(Y).forEach(function(Ue) {
          Y[Ue] = "var(".concat(Pe(Ue, at(w, L.prefix)), ")");
        });
        var We = Xe(G, {
          componentCls: Ht,
          prefixCls: b,
          iconCls: ".".concat(_),
          antCls: ".".concat(v),
          calc: W,
          // @ts-ignore
          max: q,
          // @ts-ignore
          min: Z
        }, L ? Y : Ve), zt = S(We, {
          hashId: O,
          prefixCls: b,
          rootPrefixCls: v,
          iconPrefixCls: _
        });
        Bt(w, Ve);
        var At = typeof s == "function" ? s(We, b, p, E.resetFont) : null;
        return [E.resetStyle === !1 ? null : At, zt];
      });
      return [te, O];
    };
  }
  function f(h, S, C) {
    var E = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = u(h, S, C, B({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, E)), x = function(j) {
      var g = j.prefixCls, b = j.rootCls, p = b === void 0 ? g : b;
      return m(g, p), null;
    };
    return x;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: f,
    genComponentStyleHook: u
  };
}
const $ = Math.round;
function je(t, e) {
  const n = t.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = e(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const dt = (t, e, n) => n === 0 ? t : t / 100;
function re(t, e) {
  const n = e || 255;
  return t > n ? n : t < 0 ? 0 : t;
}
class V {
  constructor(e) {
    I(this, "isValid", !0), I(this, "r", 0), I(this, "g", 0), I(this, "b", 0), I(this, "a", 1), I(this, "_h", void 0), I(this, "_s", void 0), I(this, "_l", void 0), I(this, "_v", void 0), I(this, "_max", void 0), I(this, "_min", void 0), I(this, "_brightness", void 0);
    function n(o) {
      return o[0] in e && o[1] in e && o[2] in e;
    }
    if (e) if (typeof e == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (e instanceof V)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (n("rgb"))
      this.r = re(e.r), this.g = re(e.g), this.b = re(e.b), this.a = typeof e.a == "number" ? re(e.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(e);
    else if (n("hsv"))
      this.fromHsv(e);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(e));
  }
  // ======================= Setter =======================
  setR(e) {
    return this._sc("r", e);
  }
  setG(e) {
    return this._sc("g", e);
  }
  setB(e) {
    return this._sc("b", e);
  }
  setA(e) {
    return this._sc("a", e, 1);
  }
  setHue(e) {
    const n = this.toHsv();
    return n.h = e, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = e(this.r), o = e(this.g), r = e(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = $(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._s = 0 : this._s = e / this.getMax();
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
  darken(e = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - e / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(e = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + e / 100;
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
  mix(e, n = 50) {
    const o = this._c(e), r = n / 100, i = (a) => (o[a] - this[a]) * r + this[a], s = {
      r: $(i("r")),
      g: $(i("g")),
      b: $(i("b")),
      a: $(i("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(e = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, e);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(e = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, e);
  }
  onBackground(e) {
    const n = this._c(e), o = this.a + n.a * (1 - this.a), r = (i) => $((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
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
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const n = (this.r || 0).toString(16);
    e += n.length === 2 ? n : "0" + n;
    const o = (this.g || 0).toString(16);
    e += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (e += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = $(this.a * 255).toString(16);
      e += i.length === 2 ? i : "0" + i;
    }
    return e;
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
    const e = this.getHue(), n = $(this.getSaturation() * 100), o = $(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${n}%,${o}%,${this.a})` : `hsl(${e},${n}%,${o}%)`;
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
  _sc(e, n, o) {
    const r = this.clone();
    return r[e] = re(n, o), r;
  }
  _c(e) {
    return new this.constructor(e);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(e) {
    const n = e.replace("#", "");
    function o(r, i) {
      return parseInt(n[r] + n[i || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = e % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const h = $(o * 255);
      this.r = h, this.g = h, this.b = h;
    }
    let i = 0, s = 0, a = 0;
    const l = e / 60, c = (1 - Math.abs(2 * o - 1)) * n, u = c * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = c, s = u) : l >= 1 && l < 2 ? (i = u, s = c) : l >= 2 && l < 3 ? (s = c, a = u) : l >= 3 && l < 4 ? (s = u, a = c) : l >= 4 && l < 5 ? (i = u, a = c) : l >= 5 && l < 6 && (i = c, a = u);
    const f = o - c / 2;
    this.r = $((i + f) * 255), this.g = $((s + f) * 255), this.b = $((a + f) * 255);
  }
  fromHsv({
    h: e,
    s: n,
    v: o,
    a: r
  }) {
    this._h = e % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = $(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = e / 60, a = Math.floor(s), l = s - a, c = $(o * (1 - n) * 255), u = $(o * (1 - n * l) * 255), f = $(o * (1 - n * (1 - l)) * 255);
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
  fromHsvString(e) {
    const n = je(e, dt);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(e) {
    const n = je(e, dt);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(e) {
    const n = je(e, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? $(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const vn = {
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
}, Sn = Object.assign(Object.assign({}, vn), {
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
function ke(t) {
  return t >= 0 && t <= 255;
}
function se(t, e) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new V(t).toRgb();
  if (i < 1)
    return t;
  const {
    r: s,
    g: a,
    b: l
  } = new V(e).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const u = Math.round((n - s * (1 - c)) / c), f = Math.round((o - a * (1 - c)) / c), h = Math.round((r - l * (1 - c)) / c);
    if (ke(u) && ke(f) && ke(h))
      return new V({
        r: u,
        g: f,
        b: h,
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
var xn = function(t, e) {
  var n = {};
  for (var o in t) Object.prototype.hasOwnProperty.call(t, o) && e.indexOf(o) < 0 && (n[o] = t[o]);
  if (t != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(t); r < o.length; r++)
    e.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(t, o[r]) && (n[o[r]] = t[o[r]]);
  return n;
};
function Cn(t) {
  const {
    override: e
  } = t, n = xn(t, ["override"]), o = Object.assign({}, e);
  Object.keys(Sn).forEach((h) => {
    delete o[h];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, l = 992, c = 1200, u = 1600;
  if (r.motion === !1) {
    const h = "0s";
    r.motionDurationFast = h, r.motionDurationMid = h, r.motionDurationSlow = h;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: se(r.colorBorderSecondary, r.colorBgContainer),
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
    colorErrorOutline: se(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: se(r.colorWarningBg, r.colorBgContainer),
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
    controlOutline: se(r.colorPrimaryBg, r.colorBgContainer),
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
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
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
const _n = {
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
}, wn = {
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
}, Tn = tr($e.defaultAlgorithm), En = {
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
}, Lt = (t, e, n) => {
  const o = n.getDerivativeToken(t), {
    override: r,
    ...i
  } = e;
  let s = {
    ...o,
    override: r
  };
  return s = Cn(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: c,
      ...u
    } = l;
    let f = u;
    c && (f = Lt({
      ...s,
      ...u
    }, {
      override: u
    }, c)), s[a] = f;
  }), s;
};
function Mn() {
  const {
    token: t,
    hashed: e,
    theme: n = Tn,
    override: o,
    cssVar: r
  } = d.useContext($e._internalContext), [i, s, a] = rr(n, [$e.defaultSeed, t], {
    salt: `${Wr}-${e || ""}`,
    override: o,
    getComputedToken: Lt,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: _n,
      ignore: wn,
      preserve: En
    }
  });
  return [n, a, e ? s : "", i, r];
}
const {
  genStyleHooks: Pn
} = bn({
  usePrefix: () => {
    const {
      getPrefixCls: t,
      iconPrefixCls: e
    } = he();
    return {
      iconPrefixCls: e,
      rootPrefixCls: t()
    };
  },
  useToken: () => {
    const [t, e, n, o, r] = Mn();
    return {
      theme: t,
      realToken: e,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: t
    } = he();
    return t ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var On = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, Rn = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, In = "".concat(On, " ").concat(Rn).split(/[\s\n]+/), jn = "aria-", kn = "data-";
function ht(t, e) {
  return t.indexOf(e) === 0;
}
function Ln(t) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  e === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? n = {
    aria: !0
  } : n = B({}, e);
  var o = {};
  return Object.keys(t).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || ht(r, jn)) || // Data
    n.data && ht(r, kn) || // Attr
    n.attr && In.includes(r)) && (o[r] = t[r]);
  }), o;
}
function ae(t) {
  return typeof t == "string";
}
const $n = (t, e, n, o) => {
  const r = R.useRef(""), [i, s] = R.useState(1), a = e && ae(t);
  return en(() => {
    !a && ae(t) ? s(t.length) : ae(t) && ae(r.current) && t.indexOf(r.current) !== 0 && s(1), r.current = t;
  }, [t]), R.useEffect(() => {
    if (a && i < t.length) {
      const c = setTimeout(() => {
        s((u) => u + n);
      }, o);
      return () => {
        clearTimeout(c);
      };
    }
  }, [i, e, t]), [a ? t.slice(0, i) : t, a && i < t.length];
};
function Dn(t) {
  return R.useMemo(() => {
    if (!t)
      return [!1, 0, 0, null];
    let e = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof t == "object" && (e = {
      ...e,
      ...t
    }), [!0, e.step, e.interval, e.suffix];
  }, [t]);
}
const Bn = ({
  prefixCls: t
}) => /* @__PURE__ */ d.createElement("span", {
  className: `${t}-dot`
}, /* @__PURE__ */ d.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ d.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ d.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-3"
})), Hn = (t) => {
  const {
    componentCls: e,
    paddingSM: n,
    padding: o
  } = t;
  return {
    [e]: {
      [`${e}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${oe(n)} ${oe(o)}`,
          borderRadius: t.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: t.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${t.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: t.boxShadowTertiary
        }
      }
    }
  };
}, zn = (t) => {
  const {
    componentCls: e,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    padding: i,
    calc: s
  } = t, a = s(n).mul(o).div(2).add(r).equal(), l = `${e}-content`;
  return {
    [e]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: s(i).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: t.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: t.borderRadiusXS
      }
    }
  };
}, An = (t) => {
  const {
    componentCls: e,
    padding: n
  } = t;
  return {
    [`${e}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: n,
      overflowY: "auto"
    }
  };
}, Fn = new bt("loadingMove", {
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
}), Xn = new bt("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), Nn = (t) => {
  const {
    componentCls: e,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    colorText: i,
    calc: s
  } = t;
  return {
    [e]: {
      display: "flex",
      columnGap: r,
      [`&${e}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${e}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      [`&${e}-typing ${e}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: Xn,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${e}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${e}-header, & ${e}-footer`]: {
        fontSize: n,
        lineHeight: o,
        color: t.colorText
      },
      [`& ${e}-header`]: {
        marginBottom: t.paddingXXS
      },
      [`& ${e}-footer`]: {
        marginTop: r
      },
      // =========================== Content =============================
      [`& ${e}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${e}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: i,
        fontSize: t.fontSize,
        lineHeight: t.lineHeight,
        minHeight: s(r).mul(2).add(s(o).mul(n)).equal(),
        wordBreak: "break-word",
        [`& ${e}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: t.marginXS,
          padding: `0 ${oe(t.paddingXXS)}`,
          "&-item": {
            backgroundColor: t.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: Fn,
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
}, Vn = () => ({}), $t = Pn("Bubble", (t) => {
  const e = Xe(t, {});
  return [Nn(e), An(e), Hn(e), zn(e)];
}, Vn), Dt = /* @__PURE__ */ d.createContext({}), Wn = (t, e) => {
  const {
    prefixCls: n,
    className: o,
    rootClassName: r,
    style: i,
    classNames: s = {},
    styles: a = {},
    avatar: l,
    placement: c = "start",
    loading: u = !1,
    loadingRender: f,
    typing: h,
    content: S = "",
    messageRender: C,
    variant: E = "filled",
    shape: m,
    onTypingComplete: x,
    header: w,
    footer: j,
    ...g
  } = t, {
    onUpdate: b
  } = d.useContext(Dt), p = d.useRef(null);
  d.useImperativeHandle(e, () => ({
    nativeElement: p.current
  }));
  const {
    direction: M,
    getPrefixCls: P
  } = he(), y = P("bubble", n), O = Kr("bubble"), [z, L, A, v] = Dn(h), [_, k] = $n(S, z, L, A);
  d.useEffect(() => {
    b == null || b();
  }, [_]);
  const F = d.useRef(!1);
  d.useEffect(() => {
    !k && !u ? F.current || (F.current = !0, x == null || x()) : F.current = !1;
  }, [k, u]);
  const [W, U, q] = $t(y), Z = Q(y, r, O.className, o, U, q, `${y}-${c}`, {
    [`${y}-rtl`]: M === "rtl",
    [`${y}-typing`]: k && !u && !C && !v
  }), ee = /* @__PURE__ */ d.isValidElement(l) ? l : /* @__PURE__ */ d.createElement(Zt, l), te = C ? C(_) : _;
  let X;
  u ? X = f ? f() : /* @__PURE__ */ d.createElement(Bn, {
    prefixCls: y
  }) : X = /* @__PURE__ */ d.createElement(d.Fragment, null, te, k && v);
  let G = /* @__PURE__ */ d.createElement("div", {
    style: {
      ...O.styles.content,
      ...a.content
    },
    className: Q(`${y}-content`, `${y}-content-${E}`, m && `${y}-content-${m}`, O.classNames.content, s.content)
  }, X);
  return (w || j) && (G = /* @__PURE__ */ d.createElement("div", {
    className: `${y}-content-wrapper`
  }, w && /* @__PURE__ */ d.createElement("div", {
    className: Q(`${y}-header`, O.classNames.header, s.header),
    style: {
      ...O.styles.header,
      ...a.header
    }
  }, w), G, j && /* @__PURE__ */ d.createElement("div", {
    className: Q(`${y}-footer`, O.classNames.footer, s.footer),
    style: {
      ...O.styles.footer,
      ...a.footer
    }
  }, j))), W(/* @__PURE__ */ d.createElement("div", ie({
    style: {
      ...O.style,
      ...i
    },
    className: Z
  }, g, {
    ref: p
  }), l && /* @__PURE__ */ d.createElement("div", {
    style: {
      ...O.styles.avatar,
      ...a.avatar
    },
    className: Q(`${y}-avatar`, O.classNames.avatar, s.avatar)
  }, ee), G));
}, Ne = /* @__PURE__ */ d.forwardRef(Wn);
function Un(t) {
  const [e, n] = d.useState(t.length), o = d.useMemo(() => t.slice(0, e), [t, e]), r = d.useMemo(() => {
    const s = o[o.length - 1];
    return s ? s.key : null;
  }, [o]);
  d.useEffect(() => {
    var s;
    if (!(o.length && o.every((a, l) => {
      var c;
      return a.key === ((c = t[l]) == null ? void 0 : c.key);
    }))) {
      if (o.length === 0)
        n(1);
      else
        for (let a = 0; a < o.length; a += 1)
          if (o[a].key !== ((s = t[a]) == null ? void 0 : s.key)) {
            n(a);
            break;
          }
    }
  }, [t]);
  const i = Tt((s) => {
    s === r && n(e + 1);
  });
  return [o, i];
}
function Gn(t, e) {
  const n = R.useCallback((o, r) => typeof e == "function" ? e(o, r) : e ? e[o.role] || {} : {}, [e]);
  return R.useMemo(() => (t || []).map((o, r) => {
    const i = o.key ?? `preset_${r}`;
    return {
      ...n(o, r),
      ...o,
      key: i
    };
  }), [t, n]);
}
const Kn = 1, qn = (t, e) => {
  const {
    prefixCls: n,
    rootClassName: o,
    className: r,
    items: i,
    autoScroll: s = !0,
    roles: a,
    ...l
  } = t, c = Ln(l, {
    attr: !0,
    aria: !0
  }), u = R.useRef(null), f = R.useRef({}), {
    getPrefixCls: h
  } = he(), S = h("bubble", n), C = `${S}-list`, [E, m, x] = $t(S), [w, j] = R.useState(!1);
  R.useEffect(() => (j(!0), () => {
    j(!1);
  }), []);
  const g = Gn(i, a), [b, p] = Un(g), [M, P] = R.useState(!0), [y, O] = R.useState(0), z = (v) => {
    const _ = v.target;
    P(_.scrollHeight - Math.abs(_.scrollTop) - _.clientHeight <= Kn);
  };
  R.useEffect(() => {
    s && u.current && M && u.current.scrollTo({
      top: u.current.scrollHeight
    });
  }, [y]), R.useEffect(() => {
    var v;
    if (s) {
      const _ = (v = b[b.length - 2]) == null ? void 0 : v.key, k = f.current[_];
      if (k) {
        const {
          nativeElement: F
        } = k, {
          top: W,
          bottom: U
        } = F.getBoundingClientRect(), {
          top: q,
          bottom: Z
        } = u.current.getBoundingClientRect();
        W < Z && U > q && (O((te) => te + 1), P(!0));
      }
    }
  }, [b.length]), R.useImperativeHandle(e, () => ({
    nativeElement: u.current,
    scrollTo: ({
      key: v,
      offset: _,
      behavior: k = "smooth",
      block: F
    }) => {
      if (typeof _ == "number")
        u.current.scrollTo({
          top: _,
          behavior: k
        });
      else if (v !== void 0) {
        const W = f.current[v];
        if (W) {
          const U = b.findIndex((q) => q.key === v);
          P(U === b.length - 1), W.nativeElement.scrollIntoView({
            behavior: k,
            block: F
          });
        }
      }
    }
  }));
  const L = Tt(() => {
    s && O((v) => v + 1);
  }), A = R.useMemo(() => ({
    onUpdate: L
  }), []);
  return E(/* @__PURE__ */ R.createElement(Dt.Provider, {
    value: A
  }, /* @__PURE__ */ R.createElement("div", ie({}, c, {
    className: Q(C, o, r, m, x, {
      [`${C}-reach-end`]: M
    }),
    ref: u,
    onScroll: z
  }), b.map(({
    key: v,
    ..._
  }) => /* @__PURE__ */ R.createElement(Ne, ie({}, _, {
    key: v,
    ref: (k) => {
      k ? f.current[v] = k : delete f.current[v];
    },
    typing: w ? _.typing : !1,
    onTypingComplete: () => {
      var k;
      (k = _.onTypingComplete) == null || k.call(_), p(v);
    }
  }))))));
}, Yn = /* @__PURE__ */ R.forwardRef(qn);
Ne.List = Yn;
function Qn(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Jn(t, e = !1) {
  try {
    if (qt(t))
      return t;
    if (e && !Qn(t))
      return;
    if (typeof t == "string") {
      let n = t.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function gt(t, e) {
  return yt(() => Jn(t, e), [t, e]);
}
const Zn = ({
  children: t,
  ...e
}) => /* @__PURE__ */ D.jsx(D.Fragment, {
  children: t(e)
});
function eo(t) {
  return d.createElement(Zn, {
    children: t
  });
}
function mt(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? eo((n) => /* @__PURE__ */ D.jsx(Qt, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ D.jsx(K, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...n
    })
  })) : /* @__PURE__ */ D.jsx(K, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function pt({
  key: t,
  slots: e,
  targets: n
}, o) {
  return e[t] ? (...r) => n ? n.map((i, s) => /* @__PURE__ */ D.jsx(d.Fragment, {
    children: mt(i, {
      clone: !0,
      params: r,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ D.jsx(D.Fragment, {
    children: mt(e[t], {
      clone: !0,
      params: r,
      forceClone: !0
    })
  }) : void 0;
}
const no = Ar(({
  loadingRender: t,
  messageRender: e,
  slots: n,
  setSlotParams: o,
  children: r,
  ...i
}) => {
  const s = gt(t), a = gt(e), l = yt(() => {
    var c, u;
    return n.avatar ? /* @__PURE__ */ D.jsx(K, {
      slot: n.avatar
    }) : n["avatar.icon"] || n["avatar.src"] ? {
      ...i.avatar || {},
      icon: n["avatar.icon"] ? /* @__PURE__ */ D.jsx(K, {
        slot: n["avatar.icon"]
      }) : (c = i.avatar) == null ? void 0 : c.icon,
      src: n["avatar.src"] ? /* @__PURE__ */ D.jsx(K, {
        slot: n["avatar.src"]
      }) : (u = i.avatar) == null ? void 0 : u.src
    } : i.avatar;
  }, [i.avatar, n]);
  return /* @__PURE__ */ D.jsxs(D.Fragment, {
    children: [/* @__PURE__ */ D.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ D.jsx(Ne, {
      ...i,
      avatar: l,
      typing: n["typing.suffix"] ? {
        ...de(i.typing) ? i.typing : {},
        suffix: /* @__PURE__ */ D.jsx(K, {
          slot: n["typing.suffix"]
        })
      } : i.typing,
      content: n.content ? /* @__PURE__ */ D.jsx(K, {
        slot: n.content
      }) : i.content,
      footer: n.footer ? /* @__PURE__ */ D.jsx(K, {
        slot: n.footer
      }) : i.footer,
      loadingRender: n.loadingRender ? pt({
        slots: n,
        key: "loadingRender"
      }) : s,
      messageRender: n.messageRender ? pt({
        slots: n,
        key: "messageRender"
      }) : a
    })]
  });
});
export {
  no as Bubble,
  no as default
};
