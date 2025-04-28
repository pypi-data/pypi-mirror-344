import { i as tr, a as je, r as rr, w as Y, g as nr, c as ne, b as xt } from "./Index-D6vd_yv0.js";
const F = window.ms_globals.React, v = window.ms_globals.React, Qt = window.ms_globals.React.forwardRef, Jt = window.ms_globals.React.useRef, Zt = window.ms_globals.React.useState, Yt = window.ms_globals.React.useEffect, er = window.ms_globals.React.version, re = window.ms_globals.React.useMemo, Pe = window.ms_globals.ReactDOM.createPortal, or = window.ms_globals.internalContext.useContextPropsContext, Ie = window.ms_globals.internalContext.ContextPropsProvider, St = window.ms_globals.createItemsContext.createItemsContext, ir = window.ms_globals.antd.ConfigProvider, ke = window.ms_globals.antd.theme, Ct = window.ms_globals.antd.Typography, sr = window.ms_globals.antd.Tooltip, ar = window.ms_globals.antd.Dropdown, lr = window.ms_globals.antdIcons.EllipsisOutlined, oe = window.ms_globals.antdCssinjs.unit, xe = window.ms_globals.antdCssinjs.token2CSSVar, We = window.ms_globals.antdCssinjs.useStyleRegister, cr = window.ms_globals.antdCssinjs.useCSSVarRegister, ur = window.ms_globals.antdCssinjs.createTheme, fr = window.ms_globals.antdCssinjs.useCacheToken;
var dr = /\s/;
function hr(t) {
  for (var e = t.length; e-- && dr.test(t.charAt(e)); )
    ;
  return e;
}
var gr = /^\s+/;
function mr(t) {
  return t && t.slice(0, hr(t) + 1).replace(gr, "");
}
var Ke = NaN, pr = /^[-+]0x[0-9a-f]+$/i, br = /^0b[01]+$/i, yr = /^0o[0-7]+$/i, vr = parseInt;
function qe(t) {
  if (typeof t == "number")
    return t;
  if (tr(t))
    return Ke;
  if (je(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = je(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = mr(t);
  var n = br.test(t);
  return n || yr.test(t) ? vr(t.slice(2), n ? 2 : 8) : pr.test(t) ? Ke : +t;
}
var Se = function() {
  return rr.Date.now();
}, xr = "Expected a function", Sr = Math.max, Cr = Math.min;
function _r(t, e, n) {
  var o, r, i, s, a, l, c = 0, f = !1, u = !1, d = !0;
  if (typeof t != "function")
    throw new TypeError(xr);
  e = qe(e) || 0, je(n) && (f = !!n.leading, u = "maxWait" in n, i = u ? Sr(qe(n.maxWait) || 0, e) : i, d = "trailing" in n ? !!n.trailing : d);
  function p(b) {
    var M = o, E = r;
    return o = r = void 0, c = b, s = t.apply(E, M), s;
  }
  function g(b) {
    return c = b, a = setTimeout(y, e), f ? p(b) : s;
  }
  function x(b) {
    var M = b - l, E = b - c, P = e - M;
    return u ? Cr(P, i - E) : P;
  }
  function h(b) {
    var M = b - l, E = b - c;
    return l === void 0 || M >= e || M < 0 || u && E >= i;
  }
  function y() {
    var b = Se();
    if (h(b))
      return C(b);
    a = setTimeout(y, x(b));
  }
  function C(b) {
    return a = void 0, d && o ? p(b) : (o = r = void 0, s);
  }
  function T() {
    a !== void 0 && clearTimeout(a), c = 0, o = l = r = a = void 0;
  }
  function m() {
    return a === void 0 ? s : C(Se());
  }
  function S() {
    var b = Se(), M = h(b);
    if (o = arguments, r = this, l = b, M) {
      if (a === void 0)
        return g(l);
      if (u)
        return clearTimeout(a), a = setTimeout(y, e), p(l);
    }
    return a === void 0 && (a = setTimeout(y, e)), s;
  }
  return S.cancel = T, S.flush = m, S;
}
var _t = {
  exports: {}
}, ae = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var wr = v, Tr = Symbol.for("react.element"), Mr = Symbol.for("react.fragment"), Or = Object.prototype.hasOwnProperty, Er = wr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Pr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function wt(t, e, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), e.key !== void 0 && (i = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) Or.call(e, o) && !Pr.hasOwnProperty(o) && (r[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) r[o] === void 0 && (r[o] = e[o]);
  return {
    $$typeof: Tr,
    type: t,
    key: i,
    ref: s,
    props: r,
    _owner: Er.current
  };
}
ae.Fragment = Mr;
ae.jsx = wt;
ae.jsxs = wt;
_t.exports = ae;
var I = _t.exports;
const {
  SvelteComponent: jr,
  assign: Qe,
  binding_callbacks: Je,
  check_outros: Ir,
  children: Tt,
  claim_element: Mt,
  claim_space: kr,
  component_subscribe: Ze,
  compute_slots: Lr,
  create_slot: Rr,
  detach: U,
  element: Ot,
  empty: Ye,
  exclude_internal_props: et,
  get_all_dirty_from_scope: Dr,
  get_slot_changes: Hr,
  group_outros: $r,
  init: Ar,
  insert_hydration: ee,
  safe_not_equal: zr,
  set_custom_element_data: Et,
  space: Br,
  transition_in: te,
  transition_out: Le,
  update_slot_base: Xr
} = window.__gradio__svelte__internal, {
  beforeUpdate: Fr,
  getContext: Vr,
  onDestroy: Nr,
  setContext: Gr
} = window.__gradio__svelte__internal;
function tt(t) {
  let e, n;
  const o = (
    /*#slots*/
    t[7].default
  ), r = Rr(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Ot("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      e = Mt(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Tt(e);
      r && r.l(s), s.forEach(U), this.h();
    },
    h() {
      Et(e, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      ee(i, e, s), r && r.m(e, null), t[9](e), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && Xr(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? Hr(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Dr(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (te(r, i), n = !0);
    },
    o(i) {
      Le(r, i), n = !1;
    },
    d(i) {
      i && U(e), r && r.d(i), t[9](null);
    }
  };
}
function Ur(t) {
  let e, n, o, r, i = (
    /*$$slots*/
    t[4].default && tt(t)
  );
  return {
    c() {
      e = Ot("react-portal-target"), n = Br(), i && i.c(), o = Ye(), this.h();
    },
    l(s) {
      e = Mt(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Tt(e).forEach(U), n = kr(s), i && i.l(s), o = Ye(), this.h();
    },
    h() {
      Et(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      ee(s, e, a), t[8](e), ee(s, n, a), i && i.m(s, a), ee(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && te(i, 1)) : (i = tt(s), i.c(), te(i, 1), i.m(o.parentNode, o)) : i && ($r(), Le(i, 1, 1, () => {
        i = null;
      }), Ir());
    },
    i(s) {
      r || (te(i), r = !0);
    },
    o(s) {
      Le(i), r = !1;
    },
    d(s) {
      s && (U(e), U(n), U(o)), t[8](null), i && i.d(s);
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
function Wr(t, e, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = e;
  const a = Lr(i);
  let {
    svelteInit: l
  } = e;
  const c = Y(rt(e)), f = Y();
  Ze(t, f, (m) => n(0, o = m));
  const u = Y();
  Ze(t, u, (m) => n(1, r = m));
  const d = [], p = Vr("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: x,
    subSlotIndex: h
  } = nr() || {}, y = l({
    parent: p,
    props: c,
    target: f,
    slot: u,
    slotKey: g,
    slotIndex: x,
    subSlotIndex: h,
    onDestroy(m) {
      d.push(m);
    }
  });
  Gr("$$ms-gr-react-wrapper", y), Fr(() => {
    c.set(rt(e));
  }), Nr(() => {
    d.forEach((m) => m());
  });
  function C(m) {
    Je[m ? "unshift" : "push"](() => {
      o = m, f.set(o);
    });
  }
  function T(m) {
    Je[m ? "unshift" : "push"](() => {
      r = m, u.set(r);
    });
  }
  return t.$$set = (m) => {
    n(17, e = Qe(Qe({}, e), et(m))), "svelteInit" in m && n(5, l = m.svelteInit), "$$scope" in m && n(6, s = m.$$scope);
  }, e = et(e), [o, r, f, u, a, l, s, i, C, T];
}
class Kr extends jr {
  constructor(e) {
    super(), Ar(this, e, Wr, Ur, zr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: so
} = window.__gradio__svelte__internal, nt = window.ms_globals.rerender, Ce = window.ms_globals.tree;
function qr(t, e = {}) {
  function n(o) {
    const r = Y(), i = new Kr({
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
          }, l = s.parent ?? Ce;
          return l.nodes = [...l.nodes, a], nt({
            createPortal: Pe,
            node: Ce
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== r), nt({
              createPortal: Pe,
              node: Ce
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
const Qr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Jr(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const o = t[n];
    return e[n] = Zr(n, o), e;
  }, {}) : {};
}
function Zr(t, e) {
  return typeof e == "number" && !Qr.includes(t) ? e + "px" : e;
}
function Re(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement) {
    const r = v.Children.toArray(t._reactElement.props.children).map((i) => {
      if (v.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Re(i.props.el);
        return v.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...v.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = t._reactElement.props.children, e.push(Pe(v.cloneElement(t._reactElement, {
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
      } = Re(i);
      e.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function Yr(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const Q = Qt(({
  slot: t,
  clone: e,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = Jt(), [a, l] = Zt([]), {
    forceClone: c
  } = or(), f = c ? !0 : e;
  return Yt(() => {
    var x;
    if (!s.current || !t)
      return;
    let u = t;
    function d() {
      let h = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (h = u.children[0], h.tagName.toLowerCase() === "react-portal-target" && h.children[0] && (h = h.children[0])), Yr(i, h), n && h.classList.add(...n.split(" ")), o) {
        const y = Jr(o);
        Object.keys(y).forEach((C) => {
          h.style[C] = y[C];
        });
      }
    }
    let p = null, g = null;
    if (f && window.MutationObserver) {
      let h = function() {
        var m, S, b;
        (m = s.current) != null && m.contains(u) && ((S = s.current) == null || S.removeChild(u));
        const {
          portals: C,
          clonedElement: T
        } = Re(t);
        u = T, l(C), u.style.display = "contents", g && clearTimeout(g), g = setTimeout(() => {
          d();
        }, 50), (b = s.current) == null || b.appendChild(u);
      };
      h();
      const y = _r(() => {
        h(), p == null || p.disconnect(), p == null || p.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      p = new window.MutationObserver(y), p.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (x = s.current) == null || x.appendChild(u);
    return () => {
      var h, y;
      u.style.display = "", (h = s.current) != null && h.contains(u) && ((y = s.current) == null || y.removeChild(u)), p == null || p.disconnect();
    };
  }, [t, f, n, o, i, r, c]), v.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), en = "1.1.0", tn = /* @__PURE__ */ v.createContext({}), rn = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, nn = (t) => {
  const e = v.useContext(tn);
  return v.useMemo(() => ({
    ...rn,
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
function De() {
  const {
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = v.useContext(ir.ConfigContext);
  return {
    theme: r,
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o
  };
}
function ot(t) {
  var e = F.useRef();
  e.current = t;
  var n = F.useCallback(function() {
    for (var o, r = arguments.length, i = new Array(r), s = 0; s < r; s++)
      i[s] = arguments[s];
    return (o = e.current) === null || o === void 0 ? void 0 : o.call.apply(o, [e].concat(i));
  }, []);
  return n;
}
function on(t) {
  if (Array.isArray(t)) return t;
}
function sn(t, e) {
  var n = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], l = !0, c = !1;
    try {
      if (i = (n = n.call(t)).next, e === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = i.call(n)).done) && (a.push(o.value), a.length !== e); l = !0) ;
    } catch (f) {
      c = !0, r = f;
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
function it(t, e) {
  (e == null || e > t.length) && (e = t.length);
  for (var n = 0, o = Array(e); n < e; n++) o[n] = t[n];
  return o;
}
function an(t, e) {
  if (t) {
    if (typeof t == "string") return it(t, e);
    var n = {}.toString.call(t).slice(8, -1);
    return n === "Object" && t.constructor && (n = t.constructor.name), n === "Map" || n === "Set" ? Array.from(t) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? it(t, e) : void 0;
  }
}
function ln() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function N(t, e) {
  return on(t) || sn(t, e) || an(t, e) || ln();
}
function cn() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var st = cn() ? F.useLayoutEffect : F.useEffect, un = function(e, n) {
  var o = F.useRef(!0);
  st(function() {
    return e(o.current);
  }, n), st(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, at = function(e, n) {
  un(function(o) {
    if (!o)
      return e();
  }, n);
};
function lt(t) {
  var e = F.useRef(!1), n = F.useState(t), o = N(n, 2), r = o[0], i = o[1];
  F.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function s(a, l) {
    l && e.current || i(a);
  }
  return [r, s];
}
function _e(t) {
  return t !== void 0;
}
function fn(t, e) {
  var n = e || {}, o = n.defaultValue, r = n.value, i = n.onChange, s = n.postState, a = lt(function() {
    return _e(r) ? r : _e(o) ? typeof o == "function" ? o() : o : typeof t == "function" ? t() : t;
  }), l = N(a, 2), c = l[0], f = l[1], u = r !== void 0 ? r : c, d = s ? s(u) : u, p = ot(i), g = lt([u]), x = N(g, 2), h = x[0], y = x[1];
  at(function() {
    var T = h[0];
    c !== T && p(c, T);
  }, [h]), at(function() {
    _e(r) || f(r);
  }, [r]);
  var C = ot(function(T, m) {
    f(T, m), y([u], m);
  });
  return [d, C];
}
function $(t) {
  "@babel/helpers - typeof";
  return $ = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, $(t);
}
var w = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ze = Symbol.for("react.element"), Be = Symbol.for("react.portal"), le = Symbol.for("react.fragment"), ce = Symbol.for("react.strict_mode"), ue = Symbol.for("react.profiler"), fe = Symbol.for("react.provider"), de = Symbol.for("react.context"), dn = Symbol.for("react.server_context"), he = Symbol.for("react.forward_ref"), ge = Symbol.for("react.suspense"), me = Symbol.for("react.suspense_list"), pe = Symbol.for("react.memo"), be = Symbol.for("react.lazy"), hn = Symbol.for("react.offscreen"), Pt;
Pt = Symbol.for("react.module.reference");
function H(t) {
  if (typeof t == "object" && t !== null) {
    var e = t.$$typeof;
    switch (e) {
      case ze:
        switch (t = t.type, t) {
          case le:
          case ue:
          case ce:
          case ge:
          case me:
            return t;
          default:
            switch (t = t && t.$$typeof, t) {
              case dn:
              case de:
              case he:
              case be:
              case pe:
              case fe:
                return t;
              default:
                return e;
            }
        }
      case Be:
        return e;
    }
  }
}
w.ContextConsumer = de;
w.ContextProvider = fe;
w.Element = ze;
w.ForwardRef = he;
w.Fragment = le;
w.Lazy = be;
w.Memo = pe;
w.Portal = Be;
w.Profiler = ue;
w.StrictMode = ce;
w.Suspense = ge;
w.SuspenseList = me;
w.isAsyncMode = function() {
  return !1;
};
w.isConcurrentMode = function() {
  return !1;
};
w.isContextConsumer = function(t) {
  return H(t) === de;
};
w.isContextProvider = function(t) {
  return H(t) === fe;
};
w.isElement = function(t) {
  return typeof t == "object" && t !== null && t.$$typeof === ze;
};
w.isForwardRef = function(t) {
  return H(t) === he;
};
w.isFragment = function(t) {
  return H(t) === le;
};
w.isLazy = function(t) {
  return H(t) === be;
};
w.isMemo = function(t) {
  return H(t) === pe;
};
w.isPortal = function(t) {
  return H(t) === Be;
};
w.isProfiler = function(t) {
  return H(t) === ue;
};
w.isStrictMode = function(t) {
  return H(t) === ce;
};
w.isSuspense = function(t) {
  return H(t) === ge;
};
w.isSuspenseList = function(t) {
  return H(t) === me;
};
w.isValidElementType = function(t) {
  return typeof t == "string" || typeof t == "function" || t === le || t === ue || t === ce || t === ge || t === me || t === hn || typeof t == "object" && t !== null && (t.$$typeof === be || t.$$typeof === pe || t.$$typeof === fe || t.$$typeof === de || t.$$typeof === he || t.$$typeof === Pt || t.getModuleId !== void 0);
};
w.typeOf = H;
Number(er.split(".")[0]);
function gn(t, e) {
  if ($(t) != "object" || !t) return t;
  var n = t[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(t, e);
    if ($(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function jt(t) {
  var e = gn(t, "string");
  return $(e) == "symbol" ? e : e + "";
}
function O(t, e, n) {
  return (e = jt(e)) in t ? Object.defineProperty(t, e, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = n, t;
}
function ct(t, e) {
  var n = Object.keys(t);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(t);
    e && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(t, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function L(t) {
  for (var e = 1; e < arguments.length; e++) {
    var n = arguments[e] != null ? arguments[e] : {};
    e % 2 ? ct(Object(n), !0).forEach(function(o) {
      O(t, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : ct(Object(n)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return t;
}
function ye(t, e) {
  if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function mn(t, e) {
  for (var n = 0; n < e.length; n++) {
    var o = e[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, jt(o.key), o);
  }
}
function ve(t, e, n) {
  return e && mn(t.prototype, e), Object.defineProperty(t, "prototype", {
    writable: !1
  }), t;
}
function He(t, e) {
  return He = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, He(t, e);
}
function It(t, e) {
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
function se(t) {
  return se = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, se(t);
}
function kt() {
  try {
    var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (kt = function() {
    return !!t;
  })();
}
function q(t) {
  if (t === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return t;
}
function pn(t, e) {
  if (e && ($(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return q(t);
}
function Lt(t) {
  var e = kt();
  return function() {
    var n, o = se(t);
    if (e) {
      var r = se(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return pn(this, n);
  };
}
var Rt = /* @__PURE__ */ ve(function t() {
  ye(this, t);
}), Dt = "CALC_UNIT", bn = new RegExp(Dt, "g");
function we(t) {
  return typeof t == "number" ? "".concat(t).concat(Dt) : t;
}
var yn = /* @__PURE__ */ function(t) {
  It(n, t);
  var e = Lt(n);
  function n(o, r) {
    var i;
    ye(this, n), i = e.call(this), O(q(i), "result", ""), O(q(i), "unitlessCssVar", void 0), O(q(i), "lowPriority", void 0);
    var s = $(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = we(o) : s === "string" && (i.result = o), i;
  }
  return ve(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(we(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(we(r))), this.lowPriority = !0, this;
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
      }) && (l = !1), this.result = this.result.replace(bn, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Rt), vn = /* @__PURE__ */ function(t) {
  It(n, t);
  var e = Lt(n);
  function n(o) {
    var r;
    return ye(this, n), r = e.call(this), O(q(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return ve(n, [{
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
}(Rt), xn = function(e, n) {
  var o = e === "css" ? yn : vn;
  return function(r) {
    return new o(r, n);
  };
}, ut = function(e, n) {
  return "".concat([n, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ft(t, e, n, o) {
  var r = L({}, e[t]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var l = N(a, 2), c = l[0], f = l[1];
      if (r != null && r[c] || r != null && r[f]) {
        var u;
        (u = r[f]) !== null && u !== void 0 || (r[f] = r == null ? void 0 : r[c]);
      }
    });
  }
  var s = L(L({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var Ht = typeof CSSINJS_STATISTIC < "u", $e = !0;
function Xe() {
  for (var t = arguments.length, e = new Array(t), n = 0; n < t; n++)
    e[n] = arguments[n];
  if (!Ht)
    return Object.assign.apply(Object, [{}].concat(e));
  $e = !1;
  var o = {};
  return e.forEach(function(r) {
    if ($(r) === "object") {
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
  }), $e = !0, o;
}
var dt = {};
function Sn() {
}
var Cn = function(e) {
  var n, o = e, r = Sn;
  return Ht && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(e, {
    get: function(s, a) {
      if ($e) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var l;
    dt[s] = {
      global: Array.from(n),
      component: L(L({}, (l = dt[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function ht(t, e, n) {
  if (typeof n == "function") {
    var o;
    return n(Xe(e, (o = e[t]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function _n(t) {
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
var wn = 1e3 * 60 * 10, Tn = /* @__PURE__ */ function() {
  function t() {
    ye(this, t), O(this, "map", /* @__PURE__ */ new Map()), O(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), O(this, "nextID", 0), O(this, "lastAccessBeat", /* @__PURE__ */ new Map()), O(this, "accessBeat", 0);
  }
  return ve(t, [{
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
        return i && $(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat($(i), "_").concat(i);
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
          o - r > wn && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), t;
}(), gt = new Tn();
function Mn(t, e) {
  return v.useMemo(function() {
    var n = gt.get(e);
    if (n)
      return n;
    var o = t();
    return gt.set(e, o), o;
  }, e);
}
var On = function() {
  return {};
};
function En(t) {
  var e = t.useCSP, n = e === void 0 ? On : e, o = t.useToken, r = t.usePrefix, i = t.getResetStyles, s = t.getCommonStyle, a = t.getCompUnitless;
  function l(d, p, g, x) {
    var h = Array.isArray(d) ? d[0] : d;
    function y(E) {
      return "".concat(String(h)).concat(E.slice(0, 1).toUpperCase()).concat(E.slice(1));
    }
    var C = (x == null ? void 0 : x.unitless) || {}, T = typeof a == "function" ? a(d) : {}, m = L(L({}, T), {}, O({}, y("zIndexPopup"), !0));
    Object.keys(C).forEach(function(E) {
      m[y(E)] = C[E];
    });
    var S = L(L({}, x), {}, {
      unitless: m,
      prefixToken: y
    }), b = f(d, p, g, S), M = c(h, g, S);
    return function(E) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, R = b(E, P), A = N(R, 2), _ = A[1], z = M(P), k = N(z, 2), D = k[0], B = k[1];
      return [D, _, B];
    };
  }
  function c(d, p, g) {
    var x = g.unitless, h = g.injectStyle, y = h === void 0 ? !0 : h, C = g.prefixToken, T = g.ignore, m = function(M) {
      var E = M.rootCls, P = M.cssVar, R = P === void 0 ? {} : P, A = o(), _ = A.realToken;
      return cr({
        path: [d],
        prefix: R.prefix,
        key: R.key,
        unitless: x,
        ignore: T,
        token: _,
        scope: E
      }, function() {
        var z = ht(d, _, p), k = ft(d, _, z, {
          deprecatedTokens: g == null ? void 0 : g.deprecatedTokens
        });
        return Object.keys(z).forEach(function(D) {
          k[C(D)] = k[D], delete k[D];
        }), k;
      }), null;
    }, S = function(M) {
      var E = o(), P = E.cssVar;
      return [function(R) {
        return y && P ? /* @__PURE__ */ v.createElement(v.Fragment, null, /* @__PURE__ */ v.createElement(m, {
          rootCls: M,
          cssVar: P,
          component: d
        }), R) : R;
      }, P == null ? void 0 : P.key];
    };
    return S;
  }
  function f(d, p, g) {
    var x = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = Array.isArray(d) ? d : [d, d], y = N(h, 1), C = y[0], T = h.join("-"), m = t.layer || {
      name: "antd"
    };
    return function(S) {
      var b = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : S, M = o(), E = M.theme, P = M.realToken, R = M.hashId, A = M.token, _ = M.cssVar, z = r(), k = z.rootPrefixCls, D = z.iconPrefixCls, B = n(), W = _ ? "css" : "js", Ft = Mn(function() {
        var V = /* @__PURE__ */ new Set();
        return _ && Object.keys(x.unitless || {}).forEach(function(J) {
          V.add(xe(J, _.prefix)), V.add(xe(J, ut(C, _.prefix)));
        }), xn(W, V);
      }, [W, C, _ == null ? void 0 : _.prefix]), Fe = _n(W), Vt = Fe.max, Nt = Fe.min, Ve = {
        theme: E,
        token: A,
        hashId: R,
        nonce: function() {
          return B.nonce;
        },
        clientOnly: x.clientOnly,
        layer: m,
        // antd is always at top of styles
        order: x.order || -999
      };
      typeof i == "function" && We(L(L({}, Ve), {}, {
        clientOnly: !1,
        path: ["Shared", k]
      }), function() {
        return i(A, {
          prefix: {
            rootPrefixCls: k,
            iconPrefixCls: D
          },
          csp: B
        });
      });
      var Gt = We(L(L({}, Ve), {}, {
        path: [T, S, D]
      }), function() {
        if (x.injectStyle === !1)
          return [];
        var V = Cn(A), J = V.token, Ut = V.flush, G = ht(C, P, g), Wt = ".".concat(S), Ne = ft(C, P, G, {
          deprecatedTokens: x.deprecatedTokens
        });
        _ && G && $(G) === "object" && Object.keys(G).forEach(function(Ue) {
          G[Ue] = "var(".concat(xe(Ue, ut(C, _.prefix)), ")");
        });
        var Ge = Xe(J, {
          componentCls: Wt,
          prefixCls: S,
          iconCls: ".".concat(D),
          antCls: ".".concat(k),
          calc: Ft,
          // @ts-ignore
          max: Vt,
          // @ts-ignore
          min: Nt
        }, _ ? G : Ne), Kt = p(Ge, {
          hashId: R,
          prefixCls: S,
          rootPrefixCls: k,
          iconPrefixCls: D
        });
        Ut(C, Ne);
        var qt = typeof s == "function" ? s(Ge, S, b, x.resetFont) : null;
        return [x.resetStyle === !1 ? null : qt, Kt];
      });
      return [Gt, R];
    };
  }
  function u(d, p, g) {
    var x = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = f(d, p, g, L({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, x)), y = function(T) {
      var m = T.prefixCls, S = T.rootCls, b = S === void 0 ? m : S;
      return h(m, b), null;
    };
    return y;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: u,
    genComponentStyleHook: f
  };
}
const j = Math.round;
function Te(t, e) {
  const n = t.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = e(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const mt = (t, e, n) => n === 0 ? t : t / 100;
function K(t, e) {
  const n = e || 255;
  return t > n ? n : t < 0 ? 0 : t;
}
class X {
  constructor(e) {
    O(this, "isValid", !0), O(this, "r", 0), O(this, "g", 0), O(this, "b", 0), O(this, "a", 1), O(this, "_h", void 0), O(this, "_s", void 0), O(this, "_l", void 0), O(this, "_v", void 0), O(this, "_max", void 0), O(this, "_min", void 0), O(this, "_brightness", void 0);
    function n(o) {
      return o[0] in e && o[1] in e && o[2] in e;
    }
    if (e) if (typeof e == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (e instanceof X)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (n("rgb"))
      this.r = K(e.r), this.g = K(e.g), this.b = K(e.b), this.a = typeof e.a == "number" ? K(e.a, 1) : 1;
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
      e === 0 ? this._h = 0 : this._h = j(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
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
      r: j(i("r")),
      g: j(i("g")),
      b: j(i("b")),
      a: j(i("a") * 100) / 100
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
    const n = this._c(e), o = this.a + n.a * (1 - this.a), r = (i) => j((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
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
      const i = j(this.a * 255).toString(16);
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
    const e = this.getHue(), n = j(this.getSaturation() * 100), o = j(this.getLightness() * 100);
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
    return r[e] = K(n, o), r;
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
      const d = j(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const l = e / 60, c = (1 - Math.abs(2 * o - 1)) * n, f = c * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = c, s = f) : l >= 1 && l < 2 ? (i = f, s = c) : l >= 2 && l < 3 ? (s = c, a = f) : l >= 3 && l < 4 ? (s = f, a = c) : l >= 4 && l < 5 ? (i = f, a = c) : l >= 5 && l < 6 && (i = c, a = f);
    const u = o - c / 2;
    this.r = j((i + u) * 255), this.g = j((s + u) * 255), this.b = j((a + u) * 255);
  }
  fromHsv({
    h: e,
    s: n,
    v: o,
    a: r
  }) {
    this._h = e % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = j(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = e / 60, a = Math.floor(s), l = s - a, c = j(o * (1 - n) * 255), f = j(o * (1 - n * l) * 255), u = j(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = c;
        break;
      case 1:
        this.r = f, this.b = c;
        break;
      case 2:
        this.r = c, this.b = u;
        break;
      case 3:
        this.r = c, this.g = f;
        break;
      case 4:
        this.r = u, this.g = c;
        break;
      case 5:
      default:
        this.g = c, this.b = f;
        break;
    }
  }
  fromHsvString(e) {
    const n = Te(e, mt);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(e) {
    const n = Te(e, mt);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(e) {
    const n = Te(e, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? j(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const Pn = {
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
}, jn = Object.assign(Object.assign({}, Pn), {
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
function Me(t) {
  return t >= 0 && t <= 255;
}
function Z(t, e) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new X(t).toRgb();
  if (i < 1)
    return t;
  const {
    r: s,
    g: a,
    b: l
  } = new X(e).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const f = Math.round((n - s * (1 - c)) / c), u = Math.round((o - a * (1 - c)) / c), d = Math.round((r - l * (1 - c)) / c);
    if (Me(f) && Me(u) && Me(d))
      return new X({
        r: f,
        g: u,
        b: d,
        a: Math.round(c * 100) / 100
      }).toRgbString();
  }
  return new X({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var In = function(t, e) {
  var n = {};
  for (var o in t) Object.prototype.hasOwnProperty.call(t, o) && e.indexOf(o) < 0 && (n[o] = t[o]);
  if (t != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(t); r < o.length; r++)
    e.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(t, o[r]) && (n[o[r]] = t[o[r]]);
  return n;
};
function kn(t) {
  const {
    override: e
  } = t, n = In(t, ["override"]), o = Object.assign({}, e);
  Object.keys(jn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, l = 992, c = 1200, f = 1600;
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
    colorSplit: Z(r.colorBorderSecondary, r.colorBgContainer),
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
    colorErrorOutline: Z(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: Z(r.colorWarningBg, r.colorBgContainer),
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
    controlOutline: Z(r.colorPrimaryBg, r.colorBgContainer),
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
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new X("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new X("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new X("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const Ln = {
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
}, Rn = {
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
}, Dn = ur(ke.defaultAlgorithm), Hn = {
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
}, $t = (t, e, n) => {
  const o = n.getDerivativeToken(t), {
    override: r,
    ...i
  } = e;
  let s = {
    ...o,
    override: r
  };
  return s = kn(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: c,
      ...f
    } = l;
    let u = f;
    c && (u = $t({
      ...s,
      ...f
    }, {
      override: f
    }, c)), s[a] = u;
  }), s;
};
function $n() {
  const {
    token: t,
    hashed: e,
    theme: n = Dn,
    override: o,
    cssVar: r
  } = v.useContext(ke._internalContext), [i, s, a] = fr(n, [ke.defaultSeed, t], {
    salt: `${en}-${e || ""}`,
    override: o,
    getComputedToken: $t,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: Ln,
      ignore: Rn,
      preserve: Hn
    }
  });
  return [n, a, e ? s : "", i, r];
}
const {
  genStyleHooks: An
} = En({
  usePrefix: () => {
    const {
      getPrefixCls: t,
      iconPrefixCls: e
    } = De();
    return {
      iconPrefixCls: e,
      rootPrefixCls: t()
    };
  },
  useToken: () => {
    const [t, e, n, o, r] = $n();
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
    } = De();
    return t ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var zn = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, Bn = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Xn = "".concat(zn, " ").concat(Bn).split(/[\s\n]+/), Fn = "aria-", Vn = "data-";
function pt(t, e) {
  return t.indexOf(e) === 0;
}
function At(t) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  e === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? n = {
    aria: !0
  } : n = L({}, e);
  var o = {};
  return Object.keys(t).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || pt(r, Fn)) || // Data
    n.data && pt(r, Vn) || // Attr
    n.attr && Xn.includes(r)) && (o[r] = t[r]);
  }), o;
}
const zt = /* @__PURE__ */ v.createContext(null), bt = ({
  children: t
}) => {
  const {
    prefixCls: e
  } = v.useContext(zt);
  return /* @__PURE__ */ v.createElement("div", {
    className: ne(`${e}-group-title`)
  }, t && /* @__PURE__ */ v.createElement(Ct.Text, null, t));
}, Nn = (t) => {
  t.stopPropagation();
}, Gn = (t) => {
  const {
    prefixCls: e,
    info: n,
    className: o,
    direction: r,
    onClick: i,
    active: s,
    menu: a,
    ...l
  } = t, c = At(l, {
    aria: !0,
    data: !0,
    attr: !0
  }), {
    disabled: f
  } = n, [u, d] = v.useState(!1), [p, g] = v.useState(!1), x = ne(o, `${e}-item`, {
    [`${e}-item-active`]: s && !f
  }, {
    [`${e}-item-disabled`]: f
  }), h = () => {
    !f && i && i(n);
  }, y = (S) => {
    S && g(!S);
  }, [C, T] = re(() => {
    const {
      trigger: S,
      ...b
    } = a || {};
    return [S, b];
  }, [a]), m = (S) => {
    const b = /* @__PURE__ */ v.createElement(lr, {
      onClick: Nn,
      className: `${e}-menu-icon`
    });
    return C ? typeof C == "function" ? C(S, {
      originNode: b
    }) : C : b;
  };
  return /* @__PURE__ */ v.createElement(sr, {
    title: n.label,
    open: u && p,
    onOpenChange: g,
    placement: r === "rtl" ? "left" : "right"
  }, /* @__PURE__ */ v.createElement("li", ie({}, c, {
    className: x,
    onClick: h
  }), n.icon && /* @__PURE__ */ v.createElement("div", {
    className: `${e}-icon`
  }, n.icon), /* @__PURE__ */ v.createElement(Ct.Text, {
    className: `${e}-label`,
    ellipsis: {
      onEllipsis: d
    }
  }, n.label), !f && a && /* @__PURE__ */ v.createElement(ar, {
    menu: T,
    placement: r === "rtl" ? "bottomLeft" : "bottomRight",
    trigger: ["click"],
    disabled: f,
    onOpenChange: y
  }, m(n))));
}, Oe = "__ungrouped", Un = (t, e = []) => {
  const [n, o, r] = v.useMemo(() => {
    if (!t)
      return [!1, void 0, void 0];
    let i = {
      sort: void 0,
      title: void 0
    };
    return typeof t == "object" && (i = {
      ...i,
      ...t
    }), [!0, i.sort, i.title];
  }, [t]);
  return v.useMemo(() => {
    if (!n)
      return [[{
        name: Oe,
        data: e,
        title: void 0
      }], n];
    const i = e.reduce((l, c) => {
      const f = c.group || Oe;
      return l[f] || (l[f] = []), l[f].push(c), l;
    }, {});
    return [(o ? Object.keys(i).sort(o) : Object.keys(i)).map((l) => ({
      name: l === Oe ? void 0 : l,
      title: r,
      data: i[l]
    })), n];
  }, [e, t]);
}, Wn = (t) => {
  const {
    componentCls: e
  } = t;
  return {
    [e]: {
      display: "flex",
      flexDirection: "column",
      gap: t.paddingXXS,
      overflowY: "auto",
      padding: t.paddingSM,
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      // 会话列表
      [`& ${e}-list`]: {
        display: "flex",
        gap: t.paddingXXS,
        flexDirection: "column",
        [`& ${e}-item`]: {
          paddingInlineStart: t.paddingXL
        },
        [`& ${e}-label`]: {
          color: t.colorTextDescription
        }
      },
      // 会话列表项
      [`& ${e}-item`]: {
        display: "flex",
        height: t.controlHeightLG,
        minHeight: t.controlHeightLG,
        gap: t.paddingXS,
        padding: `0 ${oe(t.paddingXS)}`,
        alignItems: "center",
        borderRadius: t.borderRadiusLG,
        cursor: "pointer",
        transition: `all ${t.motionDurationMid} ${t.motionEaseInOut}`,
        // 悬浮样式
        "&:hover": {
          backgroundColor: t.colorBgTextHover
        },
        // 选中样式
        "&-active": {
          backgroundColor: t.colorBgTextHover,
          [`& ${e}-label, ${e}-menu-icon`]: {
            color: t.colorText
          }
        },
        // 禁用样式
        "&-disabled": {
          cursor: "not-allowed",
          [`& ${e}-label`]: {
            color: t.colorTextDisabled
          }
        },
        // 悬浮、选中时激活操作菜单
        "&:hover, &-active": {
          [`& ${e}-menu-icon`]: {
            opacity: 1
          }
        }
      },
      // 会话名
      [`& ${e}-label`]: {
        flex: 1,
        color: t.colorText
      },
      // 会话操作菜单
      [`& ${e}-menu-icon`]: {
        opacity: 0,
        fontSize: t.fontSizeXL
      },
      // 会话图标
      [`& ${e}-group-title`]: {
        display: "flex",
        alignItems: "center",
        height: t.controlHeightLG,
        minHeight: t.controlHeightLG,
        padding: `0 ${oe(t.paddingXS)}`
      }
    }
  };
}, Kn = () => ({}), qn = An("Conversations", (t) => {
  const e = Xe(t, {});
  return Wn(e);
}, Kn), Qn = (t) => {
  const {
    prefixCls: e,
    rootClassName: n,
    items: o,
    activeKey: r,
    defaultActiveKey: i,
    onActiveChange: s,
    menu: a,
    styles: l = {},
    classNames: c = {},
    groupable: f,
    className: u,
    style: d,
    ...p
  } = t, g = At(p, {
    attr: !0,
    aria: !0,
    data: !0
  }), [x, h] = fn(i, {
    value: r
  }), [y, C] = Un(f, o), {
    getPrefixCls: T,
    direction: m
  } = De(), S = T("conversations", e), b = nn("conversations"), [M, E, P] = qn(S), R = ne(S, b.className, u, n, E, P, {
    [`${S}-rtl`]: m === "rtl"
  }), A = (_) => {
    h(_.key), s && s(_.key);
  };
  return M(/* @__PURE__ */ v.createElement("ul", ie({}, g, {
    style: {
      ...b.style,
      ...d
    },
    className: R
  }), y.map((_, z) => {
    var D;
    const k = _.data.map((B, W) => /* @__PURE__ */ v.createElement(Gn, {
      key: B.key || `key-${W}`,
      info: B,
      prefixCls: S,
      direction: m,
      className: ne(c.item, b.classNames.item),
      style: {
        ...b.styles.item,
        ...l.item
      },
      menu: typeof a == "function" ? a(B) : a,
      active: x === B.key,
      onClick: A
    }));
    return C ? /* @__PURE__ */ v.createElement("li", {
      key: _.name || `key-${z}`
    }, /* @__PURE__ */ v.createElement(zt.Provider, {
      value: {
        prefixCls: S
      }
    }, ((D = _.title) == null ? void 0 : D.call(_, _.name, {
      components: {
        GroupTitle: bt
      }
    })) || /* @__PURE__ */ v.createElement(bt, {
      key: _.name
    }, _.name)), /* @__PURE__ */ v.createElement("ul", {
      className: `${S}-list`
    }, k)) : k;
  })));
};
function Jn(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Bt(t, e = !1) {
  try {
    if (xt(t))
      return t;
    if (e && !Jn(t))
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
function yt(t, e) {
  return re(() => Bt(t, e), [t, e]);
}
const Zn = ({
  children: t,
  ...e
}) => /* @__PURE__ */ I.jsx(I.Fragment, {
  children: t(e)
});
function Xt(t) {
  return v.createElement(Zn, {
    children: t
  });
}
function Ae(t, e, n) {
  const o = t.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, i) => {
      var c;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const s = {
        ...r.props,
        key: ((c = r.props) == null ? void 0 : c.key) ?? (n ? `${n}-${i}` : `${i}`)
      };
      let a = s;
      Object.keys(r.slots).forEach((f) => {
        if (!r.slots[f] || !(r.slots[f] instanceof Element) && !r.slots[f].el)
          return;
        const u = f.split(".");
        u.forEach((y, C) => {
          a[y] || (a[y] = {}), C !== u.length - 1 && (a = s[y]);
        });
        const d = r.slots[f];
        let p, g, x = (e == null ? void 0 : e.clone) ?? !1, h = e == null ? void 0 : e.forceClone;
        d instanceof Element ? p = d : (p = d.el, g = d.callback, x = d.clone ?? x, h = d.forceClone ?? h), h = h ?? !!g, a[u[u.length - 1]] = p ? g ? (...y) => (g(u[u.length - 1], y), /* @__PURE__ */ I.jsx(Ie, {
          ...r.ctx,
          params: y,
          forceClone: h,
          children: /* @__PURE__ */ I.jsx(Q, {
            slot: p,
            clone: x
          })
        })) : Xt((y) => /* @__PURE__ */ I.jsx(Ie, {
          ...r.ctx,
          forceClone: h,
          children: /* @__PURE__ */ I.jsx(Q, {
            ...y,
            slot: p,
            clone: x
          })
        })) : a[u[u.length - 1]], a = s;
      });
      const l = (e == null ? void 0 : e.children) || "children";
      return r[l] ? s[l] = Ae(r[l], e, `${i}`) : e != null && e.children && (s[l] = void 0, Reflect.deleteProperty(s, l)), s;
    });
}
function vt(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? Xt((n) => /* @__PURE__ */ I.jsx(Ie, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ I.jsx(Q, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...n
    })
  })) : /* @__PURE__ */ I.jsx(Q, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Ee({
  key: t,
  slots: e,
  targets: n
}, o) {
  return e[t] ? (...r) => n ? n.map((i, s) => /* @__PURE__ */ I.jsx(v.Fragment, {
    children: vt(i, {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }, s)) : /* @__PURE__ */ I.jsx(I.Fragment, {
    children: vt(e[t], {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: Yn,
  withItemsContextProvider: eo,
  ItemHandler: ao
} = St("antd-menu-items"), {
  useItems: to,
  withItemsContextProvider: ro,
  ItemHandler: lo
} = St("antdx-conversations-items");
function no(t) {
  return typeof t == "object" && t !== null ? t : {};
}
function oo(t, e) {
  return Object.keys(t).reduce((n, o) => {
    if (o.startsWith("on") && xt(t[o])) {
      const r = t[o];
      o === "onClick" ? n[o] = (i, ...s) => {
        i.domEvent.stopPropagation(), r == null || r(e, i, ...s);
      } : n[o] = (...i) => {
        r == null || r(e, ...i);
      };
    } else
      n[o] = t[o];
    return n;
  }, {});
}
const co = qr(eo(["menu.items"], ro(["default", "items"], ({
  slots: t,
  setSlotParams: e,
  children: n,
  items: o,
  ...r
}) => {
  const {
    items: {
      "menu.items": i
    }
  } = Yn(), s = yt(r.menu), a = typeof r.groupable == "object" || t["groupable.title"], l = no(r.groupable), c = yt(r.groupable), f = re(() => {
    var p;
    if (typeof r.menu == "string")
      return s;
    {
      const g = r.menu || {};
      return ((p = g.items) == null ? void 0 : p.length) || i.length > 0 ? (h) => ({
        ...oo(g, h),
        items: g.items || Ae(i, {
          clone: !0
        }) || [],
        trigger: t["menu.trigger"] ? Ee({
          slots: t,
          key: "menu.trigger"
        }, {}) : Bt(g.trigger, !0) || g.trigger,
        expandIcon: t["menu.expandIcon"] ? Ee({
          slots: t,
          key: "menu.expandIcon"
        }, {}) : g.expandIcon,
        overflowedIndicator: t["menu.overflowedIndicator"] ? /* @__PURE__ */ I.jsx(Q, {
          slot: t["menu.overflowedIndicator"]
        }) : g.overflowedIndicator
      }) : void 0;
    }
  }, [s, i, r.menu, e, t]), {
    items: u
  } = to(), d = u.items.length > 0 ? u.items : u.default;
  return /* @__PURE__ */ I.jsxs(I.Fragment, {
    children: [/* @__PURE__ */ I.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ I.jsx(Qn, {
      ...r,
      menu: f,
      items: re(() => o || Ae(d, {
        clone: !0
      }), [o, d]),
      groupable: a ? {
        ...l,
        title: t["groupable.title"] ? Ee({
          slots: t,
          key: "groupable.title"
        }) : l.title,
        sort: c || l.sort
      } : r.groupable
    })]
  });
})));
export {
  co as Conversations,
  co as default
};
