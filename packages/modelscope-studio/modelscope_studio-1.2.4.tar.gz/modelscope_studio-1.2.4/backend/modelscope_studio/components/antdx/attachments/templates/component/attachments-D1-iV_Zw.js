import { i as fr, a as Rt, r as dr, w as We, g as pr, d as mr, b as $e, c as ie, e as hr } from "./Index-CC8-pxU5.js";
const F = window.ms_globals.React, l = window.ms_globals.React, Je = window.ms_globals.React.useMemo, qe = window.ms_globals.React.useState, we = window.ms_globals.React.useEffect, ar = window.ms_globals.React.forwardRef, ye = window.ms_globals.React.useRef, lr = window.ms_globals.React.version, cr = window.ms_globals.React.isValidElement, ur = window.ms_globals.React.useLayoutEffect, Vt = window.ms_globals.ReactDOM, Ze = window.ms_globals.ReactDOM.createPortal, gr = window.ms_globals.internalContext.useContextPropsContext, vr = window.ms_globals.internalContext.ContextPropsProvider, br = window.ms_globals.antd.ConfigProvider, Rn = window.ms_globals.antd.Upload, je = window.ms_globals.antd.theme, yr = window.ms_globals.antd.Progress, Sr = window.ms_globals.antd.Image, mt = window.ms_globals.antd.Button, wr = window.ms_globals.antd.Flex, ht = window.ms_globals.antd.Typography, xr = window.ms_globals.antdIcons.FileTextFilled, Er = window.ms_globals.antdIcons.CloseCircleFilled, Cr = window.ms_globals.antdIcons.FileExcelFilled, _r = window.ms_globals.antdIcons.FileImageFilled, Lr = window.ms_globals.antdIcons.FileMarkdownFilled, Rr = window.ms_globals.antdIcons.FilePdfFilled, Ir = window.ms_globals.antdIcons.FilePptFilled, Tr = window.ms_globals.antdIcons.FileWordFilled, Pr = window.ms_globals.antdIcons.FileZipFilled, Mr = window.ms_globals.antdIcons.PlusOutlined, Or = window.ms_globals.antdIcons.LeftOutlined, Fr = window.ms_globals.antdIcons.RightOutlined, Xt = window.ms_globals.antdCssinjs.unit, gt = window.ms_globals.antdCssinjs.token2CSSVar, Wt = window.ms_globals.antdCssinjs.useStyleRegister, Ar = window.ms_globals.antdCssinjs.useCSSVarRegister, $r = window.ms_globals.antdCssinjs.createTheme, kr = window.ms_globals.antdCssinjs.useCacheToken;
var jr = /\s/;
function Dr(e) {
  for (var t = e.length; t-- && jr.test(e.charAt(t)); )
    ;
  return t;
}
var Nr = /^\s+/;
function zr(e) {
  return e && e.slice(0, Dr(e) + 1).replace(Nr, "");
}
var Gt = NaN, Hr = /^[-+]0x[0-9a-f]+$/i, Ur = /^0b[01]+$/i, Br = /^0o[0-7]+$/i, Vr = parseInt;
function Kt(e) {
  if (typeof e == "number")
    return e;
  if (fr(e))
    return Gt;
  if (Rt(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Rt(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = zr(e);
  var n = Ur.test(e);
  return n || Br.test(e) ? Vr(e.slice(2), n ? 2 : 8) : Hr.test(e) ? Gt : +e;
}
function Xr() {
}
var vt = function() {
  return dr.Date.now();
}, Wr = "Expected a function", Gr = Math.max, Kr = Math.min;
function qr(e, t, n) {
  var r, o, i, s, a, c, u = 0, p = !1, f = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Wr);
  t = Kt(t) || 0, Rt(n) && (p = !!n.leading, f = "maxWait" in n, i = f ? Gr(Kt(n.maxWait) || 0, t) : i, d = "trailing" in n ? !!n.trailing : d);
  function m(v) {
    var L = r, S = o;
    return r = o = void 0, u = v, s = e.apply(S, L), s;
  }
  function y(v) {
    return u = v, a = setTimeout(b, t), p ? m(v) : s;
  }
  function w(v) {
    var L = v - c, S = v - u, T = t - L;
    return f ? Kr(T, i - S) : T;
  }
  function h(v) {
    var L = v - c, S = v - u;
    return c === void 0 || L >= t || L < 0 || f && S >= i;
  }
  function b() {
    var v = vt();
    if (h(v))
      return E(v);
    a = setTimeout(b, w(v));
  }
  function E(v) {
    return a = void 0, d && r ? m(v) : (r = o = void 0, s);
  }
  function C() {
    a !== void 0 && clearTimeout(a), u = 0, r = c = o = a = void 0;
  }
  function g() {
    return a === void 0 ? s : E(vt());
  }
  function x() {
    var v = vt(), L = h(v);
    if (r = arguments, o = this, c = v, L) {
      if (a === void 0)
        return y(c);
      if (f)
        return clearTimeout(a), a = setTimeout(b, t), m(c);
    }
    return a === void 0 && (a = setTimeout(b, t)), s;
  }
  return x.cancel = C, x.flush = g, x;
}
var In = {
  exports: {}
}, et = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Zr = l, Qr = Symbol.for("react.element"), Yr = Symbol.for("react.fragment"), Jr = Object.prototype.hasOwnProperty, eo = Zr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, to = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Tn(e, t, n) {
  var r, o = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) Jr.call(t, r) && !to.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Qr,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: eo.current
  };
}
et.Fragment = Yr;
et.jsx = Tn;
et.jsxs = Tn;
In.exports = et;
var te = In.exports;
const {
  SvelteComponent: no,
  assign: qt,
  binding_callbacks: Zt,
  check_outros: ro,
  children: Pn,
  claim_element: Mn,
  claim_space: oo,
  component_subscribe: Qt,
  compute_slots: io,
  create_slot: so,
  detach: Ce,
  element: On,
  empty: Yt,
  exclude_internal_props: Jt,
  get_all_dirty_from_scope: ao,
  get_slot_changes: lo,
  group_outros: co,
  init: uo,
  insert_hydration: Ge,
  safe_not_equal: fo,
  set_custom_element_data: Fn,
  space: po,
  transition_in: Ke,
  transition_out: It,
  update_slot_base: mo
} = window.__gradio__svelte__internal, {
  beforeUpdate: ho,
  getContext: go,
  onDestroy: vo,
  setContext: bo
} = window.__gradio__svelte__internal;
function en(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), o = so(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = On("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = Mn(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Pn(t);
      o && o.l(s), s.forEach(Ce), this.h();
    },
    h() {
      Fn(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Ge(i, t, s), o && o.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && mo(
        o,
        r,
        i,
        /*$$scope*/
        i[6],
        n ? lo(
          r,
          /*$$scope*/
          i[6],
          s,
          null
        ) : ao(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (Ke(o, i), n = !0);
    },
    o(i) {
      It(o, i), n = !1;
    },
    d(i) {
      i && Ce(t), o && o.d(i), e[9](null);
    }
  };
}
function yo(e) {
  let t, n, r, o, i = (
    /*$$slots*/
    e[4].default && en(e)
  );
  return {
    c() {
      t = On("react-portal-target"), n = po(), i && i.c(), r = Yt(), this.h();
    },
    l(s) {
      t = Mn(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Pn(t).forEach(Ce), n = oo(s), i && i.l(s), r = Yt(), this.h();
    },
    h() {
      Fn(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Ge(s, t, a), e[8](t), Ge(s, n, a), i && i.m(s, a), Ge(s, r, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && Ke(i, 1)) : (i = en(s), i.c(), Ke(i, 1), i.m(r.parentNode, r)) : i && (co(), It(i, 1, 1, () => {
        i = null;
      }), ro());
    },
    i(s) {
      o || (Ke(i), o = !0);
    },
    o(s) {
      It(i), o = !1;
    },
    d(s) {
      s && (Ce(t), Ce(n), Ce(r)), e[8](null), i && i.d(s);
    }
  };
}
function tn(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function So(e, t, n) {
  let r, o, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = io(i);
  let {
    svelteInit: c
  } = t;
  const u = We(tn(t)), p = We();
  Qt(e, p, (g) => n(0, r = g));
  const f = We();
  Qt(e, f, (g) => n(1, o = g));
  const d = [], m = go("$$ms-gr-react-wrapper"), {
    slotKey: y,
    slotIndex: w,
    subSlotIndex: h
  } = pr() || {}, b = c({
    parent: m,
    props: u,
    target: p,
    slot: f,
    slotKey: y,
    slotIndex: w,
    subSlotIndex: h,
    onDestroy(g) {
      d.push(g);
    }
  });
  bo("$$ms-gr-react-wrapper", b), ho(() => {
    u.set(tn(t));
  }), vo(() => {
    d.forEach((g) => g());
  });
  function E(g) {
    Zt[g ? "unshift" : "push"](() => {
      r = g, p.set(r);
    });
  }
  function C(g) {
    Zt[g ? "unshift" : "push"](() => {
      o = g, f.set(o);
    });
  }
  return e.$$set = (g) => {
    n(17, t = qt(qt({}, t), Jt(g))), "svelteInit" in g && n(5, c = g.svelteInit), "$$scope" in g && n(6, s = g.$$scope);
  }, t = Jt(t), [r, o, p, f, a, c, s, i, E, C];
}
class wo extends no {
  constructor(t) {
    super(), uo(this, t, So, yo, fo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: hs
} = window.__gradio__svelte__internal, nn = window.ms_globals.rerender, bt = window.ms_globals.tree;
function xo(e, t = {}) {
  function n(r) {
    const o = We(), i = new wo({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? bt;
          return c.nodes = [...c.nodes, a], nn({
            createPortal: Ze,
            node: bt
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), nn({
              createPortal: Ze,
              node: bt
            });
          }), a;
        },
        ...r.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
function Eo(e) {
  const [t, n] = qe(() => $e(e));
  return we(() => {
    let r = !0;
    return e.subscribe((i) => {
      r && (r = !1, i === t) || n(i);
    });
  }, [e]), t;
}
function Co(e) {
  const t = Je(() => mr(e, (n) => n), [e]);
  return Eo(t);
}
const _o = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Lo(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return t[n] = Ro(n, r), t;
  }, {}) : {};
}
function Ro(e, t) {
  return typeof t == "number" && !_o.includes(e) ? t + "px" : t;
}
function Tt(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const o = l.Children.toArray(e._reactElement.props.children).map((i) => {
      if (l.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Tt(i.props.el);
        return l.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...l.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(Ze(l.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      n.addEventListener(a, s, c);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const i = r[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Tt(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Io(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const ke = ar(({
  slot: e,
  clone: t,
  className: n,
  style: r,
  observeAttributes: o
}, i) => {
  const s = ye(), [a, c] = qe([]), {
    forceClone: u
  } = gr(), p = u ? !0 : t;
  return we(() => {
    var w;
    if (!s.current || !e)
      return;
    let f = e;
    function d() {
      let h = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (h = f.children[0], h.tagName.toLowerCase() === "react-portal-target" && h.children[0] && (h = h.children[0])), Io(i, h), n && h.classList.add(...n.split(" ")), r) {
        const b = Lo(r);
        Object.keys(b).forEach((E) => {
          h.style[E] = b[E];
        });
      }
    }
    let m = null, y = null;
    if (p && window.MutationObserver) {
      let h = function() {
        var g, x, v;
        (g = s.current) != null && g.contains(f) && ((x = s.current) == null || x.removeChild(f));
        const {
          portals: E,
          clonedElement: C
        } = Tt(e);
        f = C, c(E), f.style.display = "contents", y && clearTimeout(y), y = setTimeout(() => {
          d();
        }, 50), (v = s.current) == null || v.appendChild(f);
      };
      h();
      const b = qr(() => {
        h(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      m = new window.MutationObserver(b), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (w = s.current) == null || w.appendChild(f);
    return () => {
      var h, b;
      f.style.display = "", (h = s.current) != null && h.contains(f) && ((b = s.current) == null || b.removeChild(f)), m == null || m.disconnect();
    };
  }, [e, p, n, r, i, o, u]), l.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), To = "1.1.0", Po = /* @__PURE__ */ l.createContext({}), Mo = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Oo = (e) => {
  const t = l.useContext(Po);
  return l.useMemo(() => ({
    ...Mo,
    ...t[e]
  }), [t[e]]);
};
function Re() {
  return Re = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, Re.apply(null, arguments);
}
function Qe() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r,
    theme: o
  } = l.useContext(br.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r
  };
}
function Ie(e) {
  var t = F.useRef();
  t.current = e;
  var n = F.useCallback(function() {
    for (var r, o = arguments.length, i = new Array(o), s = 0; s < o; s++)
      i[s] = arguments[s];
    return (r = t.current) === null || r === void 0 ? void 0 : r.call.apply(r, [t].concat(i));
  }, []);
  return n;
}
function Fo(e) {
  if (Array.isArray(e)) return e;
}
function Ao(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var r, o, i, s, a = [], c = !0, u = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        c = !1;
      } else for (; !(c = (r = i.call(n)).done) && (a.push(r.value), a.length !== t); c = !0) ;
    } catch (p) {
      u = !0, o = p;
    } finally {
      try {
        if (!c && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function rn(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
  return r;
}
function $o(e, t) {
  if (e) {
    if (typeof e == "string") return rn(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? rn(e, t) : void 0;
  }
}
function ko() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ee(e, t) {
  return Fo(e) || Ao(e, t) || $o(e, t) || ko();
}
function tt() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var on = tt() ? F.useLayoutEffect : F.useEffect, jo = function(t, n) {
  var r = F.useRef(!0);
  on(function() {
    return t(r.current);
  }, n), on(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, sn = function(t, n) {
  jo(function(r) {
    if (!r)
      return t();
  }, n);
};
function De(e) {
  var t = F.useRef(!1), n = F.useState(e), r = ee(n, 2), o = r[0], i = r[1];
  F.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, c) {
    c && t.current || i(a);
  }
  return [o, s];
}
function yt(e) {
  return e !== void 0;
}
function Do(e, t) {
  var n = t || {}, r = n.defaultValue, o = n.value, i = n.onChange, s = n.postState, a = De(function() {
    return yt(o) ? o : yt(r) ? typeof r == "function" ? r() : r : typeof e == "function" ? e() : e;
  }), c = ee(a, 2), u = c[0], p = c[1], f = o !== void 0 ? o : u, d = s ? s(f) : f, m = Ie(i), y = De([f]), w = ee(y, 2), h = w[0], b = w[1];
  sn(function() {
    var C = h[0];
    u !== C && m(u, C);
  }, [h]), sn(function() {
    yt(o) || p(o);
  }, [o]);
  var E = Ie(function(C, g) {
    p(C, g), b([f], g);
  });
  return [d, E];
}
function Z(e) {
  "@babel/helpers - typeof";
  return Z = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Z(e);
}
var An = {
  exports: {}
}, A = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Nt = Symbol.for("react.element"), zt = Symbol.for("react.portal"), nt = Symbol.for("react.fragment"), rt = Symbol.for("react.strict_mode"), ot = Symbol.for("react.profiler"), it = Symbol.for("react.provider"), st = Symbol.for("react.context"), No = Symbol.for("react.server_context"), at = Symbol.for("react.forward_ref"), lt = Symbol.for("react.suspense"), ct = Symbol.for("react.suspense_list"), ut = Symbol.for("react.memo"), ft = Symbol.for("react.lazy"), zo = Symbol.for("react.offscreen"), $n;
$n = Symbol.for("react.module.reference");
function se(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Nt:
        switch (e = e.type, e) {
          case nt:
          case ot:
          case rt:
          case lt:
          case ct:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case No:
              case st:
              case at:
              case ft:
              case ut:
              case it:
                return e;
              default:
                return t;
            }
        }
      case zt:
        return t;
    }
  }
}
A.ContextConsumer = st;
A.ContextProvider = it;
A.Element = Nt;
A.ForwardRef = at;
A.Fragment = nt;
A.Lazy = ft;
A.Memo = ut;
A.Portal = zt;
A.Profiler = ot;
A.StrictMode = rt;
A.Suspense = lt;
A.SuspenseList = ct;
A.isAsyncMode = function() {
  return !1;
};
A.isConcurrentMode = function() {
  return !1;
};
A.isContextConsumer = function(e) {
  return se(e) === st;
};
A.isContextProvider = function(e) {
  return se(e) === it;
};
A.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Nt;
};
A.isForwardRef = function(e) {
  return se(e) === at;
};
A.isFragment = function(e) {
  return se(e) === nt;
};
A.isLazy = function(e) {
  return se(e) === ft;
};
A.isMemo = function(e) {
  return se(e) === ut;
};
A.isPortal = function(e) {
  return se(e) === zt;
};
A.isProfiler = function(e) {
  return se(e) === ot;
};
A.isStrictMode = function(e) {
  return se(e) === rt;
};
A.isSuspense = function(e) {
  return se(e) === lt;
};
A.isSuspenseList = function(e) {
  return se(e) === ct;
};
A.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === nt || e === ot || e === rt || e === lt || e === ct || e === zo || typeof e == "object" && e !== null && (e.$$typeof === ft || e.$$typeof === ut || e.$$typeof === it || e.$$typeof === st || e.$$typeof === at || e.$$typeof === $n || e.getModuleId !== void 0);
};
A.typeOf = se;
An.exports = A;
var St = An.exports, Ho = Symbol.for("react.element"), Uo = Symbol.for("react.transitional.element"), Bo = Symbol.for("react.fragment");
function Vo(e) {
  return (
    // Base object type
    e && Z(e) === "object" && // React Element type
    (e.$$typeof === Ho || e.$$typeof === Uo) && // React Fragment type
    e.type === Bo
  );
}
var Xo = Number(lr.split(".")[0]), Wo = function(t, n) {
  typeof t == "function" ? t(n) : Z(t) === "object" && t && "current" in t && (t.current = n);
}, Go = function(t) {
  var n, r;
  if (!t)
    return !1;
  if (kn(t) && Xo >= 19)
    return !0;
  var o = St.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((n = o.prototype) !== null && n !== void 0 && n.render) && o.$$typeof !== St.ForwardRef || typeof t == "function" && !((r = t.prototype) !== null && r !== void 0 && r.render) && t.$$typeof !== St.ForwardRef);
};
function kn(e) {
  return /* @__PURE__ */ cr(e) && !Vo(e);
}
var Ko = function(t) {
  if (t && kn(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function qo(e, t) {
  if (Z(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t);
    if (Z(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function jn(e) {
  var t = qo(e, "string");
  return Z(t) == "symbol" ? t : t + "";
}
function I(e, t, n) {
  return (t = jn(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function an(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e);
    t && (r = r.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), n.push.apply(n, r);
  }
  return n;
}
function R(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? an(Object(n), !0).forEach(function(r) {
      I(e, r, n[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : an(Object(n)).forEach(function(r) {
      Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r));
    });
  }
  return e;
}
const Ne = /* @__PURE__ */ l.createContext(null);
function ln(e) {
  const {
    getDropContainer: t,
    className: n,
    prefixCls: r,
    children: o
  } = e, {
    disabled: i
  } = l.useContext(Ne), [s, a] = l.useState(), [c, u] = l.useState(null);
  if (l.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && a(d);
  }, [t]), l.useEffect(() => {
    if (s) {
      const d = () => {
        u(!0);
      }, m = (h) => {
        h.preventDefault();
      }, y = (h) => {
        h.relatedTarget || u(!1);
      }, w = (h) => {
        u(!1), h.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", m), document.addEventListener("dragleave", y), document.addEventListener("drop", w), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", m), document.removeEventListener("dragleave", y), document.removeEventListener("drop", w);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const f = `${r}-drop-area`;
  return /* @__PURE__ */ Ze(/* @__PURE__ */ l.createElement("div", {
    className: ie(f, n, {
      [`${f}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, o), s);
}
function cn(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function Zo(e) {
  return e && Z(e) === "object" && cn(e.nativeElement) ? e.nativeElement : cn(e) ? e : null;
}
function Qo(e) {
  var t = Zo(e);
  if (t)
    return t;
  if (e instanceof l.Component) {
    var n;
    return (n = Vt.findDOMNode) === null || n === void 0 ? void 0 : n.call(Vt, e);
  }
  return null;
}
function Yo(e, t) {
  if (e == null) return {};
  var n = {};
  for (var r in e) if ({}.hasOwnProperty.call(e, r)) {
    if (t.indexOf(r) !== -1) continue;
    n[r] = e[r];
  }
  return n;
}
function un(e, t) {
  if (e == null) return {};
  var n, r, o = Yo(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (r = 0; r < i.length; r++) n = i[r], t.indexOf(n) === -1 && {}.propertyIsEnumerable.call(e, n) && (o[n] = e[n]);
  }
  return o;
}
var Jo = /* @__PURE__ */ F.createContext({});
function Te(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function fn(e, t) {
  for (var n = 0; n < t.length; n++) {
    var r = t[n];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, jn(r.key), r);
  }
}
function Pe(e, t, n) {
  return t && fn(e.prototype, t), n && fn(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Pt(e, t) {
  return Pt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Pt(e, t);
}
function dt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Pt(e, t);
}
function Ye(e) {
  return Ye = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Ye(e);
}
function Dn() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Dn = function() {
    return !!e;
  })();
}
function xe(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function ei(e, t) {
  if (t && (Z(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return xe(e);
}
function pt(e) {
  var t = Dn();
  return function() {
    var n, r = Ye(e);
    if (t) {
      var o = Ye(this).constructor;
      n = Reflect.construct(r, arguments, o);
    } else n = r.apply(this, arguments);
    return ei(this, n);
  };
}
var ti = /* @__PURE__ */ function(e) {
  dt(n, e);
  var t = pt(n);
  function n() {
    return Te(this, n), t.apply(this, arguments);
  }
  return Pe(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(F.Component);
function ni(e) {
  var t = F.useReducer(function(a) {
    return a + 1;
  }, 0), n = ee(t, 2), r = n[1], o = F.useRef(e), i = Ie(function() {
    return o.current;
  }), s = Ie(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, r();
  });
  return [i, s];
}
var be = "none", ze = "appear", He = "enter", Ue = "leave", dn = "none", ce = "prepare", _e = "start", Le = "active", Ht = "end", Nn = "prepared";
function pn(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function ri(e, t) {
  var n = {
    animationend: pn("Animation", "AnimationEnd"),
    transitionend: pn("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var oi = ri(tt(), typeof window < "u" ? window : {}), zn = {};
if (tt()) {
  var ii = document.createElement("div");
  zn = ii.style;
}
var Be = {};
function Hn(e) {
  if (Be[e])
    return Be[e];
  var t = oi[e];
  if (t)
    for (var n = Object.keys(t), r = n.length, o = 0; o < r; o += 1) {
      var i = n[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in zn)
        return Be[e] = t[i], Be[e];
    }
  return "";
}
var Un = Hn("animationend"), Bn = Hn("transitionend"), Vn = !!(Un && Bn), mn = Un || "animationend", hn = Bn || "transitionend";
function gn(e, t) {
  if (!e) return null;
  if (Z(e) === "object") {
    var n = t.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const si = function(e) {
  var t = ye();
  function n(o) {
    o && (o.removeEventListener(hn, e), o.removeEventListener(mn, e));
  }
  function r(o) {
    t.current && t.current !== o && n(t.current), o && o !== t.current && (o.addEventListener(hn, e), o.addEventListener(mn, e), t.current = o);
  }
  return F.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [r, n];
};
var Xn = tt() ? ur : we, Wn = function(t) {
  return +setTimeout(t, 16);
}, Gn = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Wn = function(t) {
  return window.requestAnimationFrame(t);
}, Gn = function(t) {
  return window.cancelAnimationFrame(t);
});
var vn = 0, Ut = /* @__PURE__ */ new Map();
function Kn(e) {
  Ut.delete(e);
}
var Mt = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  vn += 1;
  var r = vn;
  function o(i) {
    if (i === 0)
      Kn(r), t();
    else {
      var s = Wn(function() {
        o(i - 1);
      });
      Ut.set(r, s);
    }
  }
  return o(n), r;
};
Mt.cancel = function(e) {
  var t = Ut.get(e);
  return Kn(e), Gn(t);
};
const ai = function() {
  var e = F.useRef(null);
  function t() {
    Mt.cancel(e.current);
  }
  function n(r) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = Mt(function() {
      o <= 1 ? r({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(r, o - 1);
    });
    e.current = i;
  }
  return F.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var li = [ce, _e, Le, Ht], ci = [ce, Nn], qn = !1, ui = !0;
function Zn(e) {
  return e === Le || e === Ht;
}
const fi = function(e, t, n) {
  var r = De(dn), o = ee(r, 2), i = o[0], s = o[1], a = ai(), c = ee(a, 2), u = c[0], p = c[1];
  function f() {
    s(ce, !0);
  }
  var d = t ? ci : li;
  return Xn(function() {
    if (i !== dn && i !== Ht) {
      var m = d.indexOf(i), y = d[m + 1], w = n(i);
      w === qn ? s(y, !0) : y && u(function(h) {
        function b() {
          h.isCanceled() || s(y, !0);
        }
        w === !0 ? b() : Promise.resolve(w).then(b);
      });
    }
  }, [e, i]), F.useEffect(function() {
    return function() {
      p();
    };
  }, []), [f, i];
};
function di(e, t, n, r) {
  var o = r.motionEnter, i = o === void 0 ? !0 : o, s = r.motionAppear, a = s === void 0 ? !0 : s, c = r.motionLeave, u = c === void 0 ? !0 : c, p = r.motionDeadline, f = r.motionLeaveImmediately, d = r.onAppearPrepare, m = r.onEnterPrepare, y = r.onLeavePrepare, w = r.onAppearStart, h = r.onEnterStart, b = r.onLeaveStart, E = r.onAppearActive, C = r.onEnterActive, g = r.onLeaveActive, x = r.onAppearEnd, v = r.onEnterEnd, L = r.onLeaveEnd, S = r.onVisibleChanged, T = De(), $ = ee(T, 2), k = $[0], _ = $[1], M = ni(be), P = ee(M, 2), O = P[0], j = P[1], H = De(null), Q = ee(H, 2), pe = Q[0], ue = Q[1], X = O(), D = ye(!1), K = ye(null);
  function z() {
    return n();
  }
  var Y = ye(!1);
  function me() {
    j(be), ue(null, !0);
  }
  var ae = Ie(function(W) {
    var V = O();
    if (V !== be) {
      var re = z();
      if (!(W && !W.deadline && W.target !== re)) {
        var ve = Y.current, N;
        V === ze && ve ? N = x == null ? void 0 : x(re, W) : V === He && ve ? N = v == null ? void 0 : v(re, W) : V === Ue && ve && (N = L == null ? void 0 : L(re, W)), ve && N !== !1 && me();
      }
    }
  }), Me = si(ae), Ee = ee(Me, 1), he = Ee[0], fe = function(V) {
    switch (V) {
      case ze:
        return I(I(I({}, ce, d), _e, w), Le, E);
      case He:
        return I(I(I({}, ce, m), _e, h), Le, C);
      case Ue:
        return I(I(I({}, ce, y), _e, b), Le, g);
      default:
        return {};
    }
  }, le = F.useMemo(function() {
    return fe(X);
  }, [X]), Se = fi(X, !e, function(W) {
    if (W === ce) {
      var V = le[ce];
      return V ? V(z()) : qn;
    }
    if (B in le) {
      var re;
      ue(((re = le[B]) === null || re === void 0 ? void 0 : re.call(le, z(), null)) || null);
    }
    return B === Le && X !== be && (he(z()), p > 0 && (clearTimeout(K.current), K.current = setTimeout(function() {
      ae({
        deadline: !0
      });
    }, p))), B === Nn && me(), ui;
  }), Oe = ee(Se, 2), Fe = Oe[0], B = Oe[1], U = Zn(B);
  Y.current = U;
  var ne = ye(null);
  Xn(function() {
    if (!(D.current && ne.current === t)) {
      _(t);
      var W = D.current;
      D.current = !0;
      var V;
      !W && t && a && (V = ze), W && t && i && (V = He), (W && !t && u || !W && f && !t && u) && (V = Ue);
      var re = fe(V);
      V && (e || re[ce]) ? (j(V), Fe()) : j(be), ne.current = t;
    }
  }, [t]), we(function() {
    // Cancel appear
    (X === ze && !a || // Cancel enter
    X === He && !i || // Cancel leave
    X === Ue && !u) && j(be);
  }, [a, i, u]), we(function() {
    return function() {
      D.current = !1, clearTimeout(K.current);
    };
  }, []);
  var ge = F.useRef(!1);
  we(function() {
    k && (ge.current = !0), k !== void 0 && X === be && ((ge.current || k) && (S == null || S(k)), ge.current = !0);
  }, [k, X]);
  var q = pe;
  return le[ce] && B === _e && (q = R({
    transition: "none"
  }, q)), [X, B, q, k ?? t];
}
function pi(e) {
  var t = e;
  Z(e) === "object" && (t = e.transitionSupport);
  function n(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var r = /* @__PURE__ */ F.forwardRef(function(o, i) {
    var s = o.visible, a = s === void 0 ? !0 : s, c = o.removeOnLeave, u = c === void 0 ? !0 : c, p = o.forceRender, f = o.children, d = o.motionName, m = o.leavedClassName, y = o.eventProps, w = F.useContext(Jo), h = w.motion, b = n(o, h), E = ye(), C = ye();
    function g() {
      try {
        return E.current instanceof HTMLElement ? E.current : Qo(C.current);
      } catch {
        return null;
      }
    }
    var x = di(b, a, g, o), v = ee(x, 4), L = v[0], S = v[1], T = v[2], $ = v[3], k = F.useRef($);
    $ && (k.current = !0);
    var _ = F.useCallback(function(Q) {
      E.current = Q, Wo(i, Q);
    }, [i]), M, P = R(R({}, y), {}, {
      visible: a
    });
    if (!f)
      M = null;
    else if (L === be)
      $ ? M = f(R({}, P), _) : !u && k.current && m ? M = f(R(R({}, P), {}, {
        className: m
      }), _) : p || !u && !m ? M = f(R(R({}, P), {}, {
        style: {
          display: "none"
        }
      }), _) : M = null;
    else {
      var O;
      S === ce ? O = "prepare" : Zn(S) ? O = "active" : S === _e && (O = "start");
      var j = gn(d, "".concat(L, "-").concat(O));
      M = f(R(R({}, P), {}, {
        className: ie(gn(d, L), I(I({}, j, j && O), d, typeof d == "string")),
        style: T
      }), _);
    }
    if (/* @__PURE__ */ F.isValidElement(M) && Go(M)) {
      var H = Ko(M);
      H || (M = /* @__PURE__ */ F.cloneElement(M, {
        ref: _
      }));
    }
    return /* @__PURE__ */ F.createElement(ti, {
      ref: C
    }, M);
  });
  return r.displayName = "CSSMotion", r;
}
const mi = pi(Vn);
var Ot = "add", Ft = "keep", At = "remove", wt = "removed";
function hi(e) {
  var t;
  return e && Z(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, R(R({}, t), {}, {
    key: String(t.key)
  });
}
function $t() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(hi);
}
function gi() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], r = 0, o = t.length, i = $t(e), s = $t(t);
  i.forEach(function(u) {
    for (var p = !1, f = r; f < o; f += 1) {
      var d = s[f];
      if (d.key === u.key) {
        r < f && (n = n.concat(s.slice(r, f).map(function(m) {
          return R(R({}, m), {}, {
            status: Ot
          });
        })), r = f), n.push(R(R({}, d), {}, {
          status: Ft
        })), r += 1, p = !0;
        break;
      }
    }
    p || n.push(R(R({}, u), {}, {
      status: At
    }));
  }), r < o && (n = n.concat(s.slice(r).map(function(u) {
    return R(R({}, u), {}, {
      status: Ot
    });
  })));
  var a = {};
  n.forEach(function(u) {
    var p = u.key;
    a[p] = (a[p] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return c.forEach(function(u) {
    n = n.filter(function(p) {
      var f = p.key, d = p.status;
      return f !== u || d !== At;
    }), n.forEach(function(p) {
      p.key === u && (p.status = Ft);
    });
  }), n;
}
var vi = ["component", "children", "onVisibleChanged", "onAllRemoved"], bi = ["status"], yi = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function Si(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : mi, n = /* @__PURE__ */ function(r) {
    dt(i, r);
    var o = pt(i);
    function i() {
      var s;
      Te(this, i);
      for (var a = arguments.length, c = new Array(a), u = 0; u < a; u++)
        c[u] = arguments[u];
      return s = o.call.apply(o, [this].concat(c)), I(xe(s), "state", {
        keyEntities: []
      }), I(xe(s), "removeKey", function(p) {
        s.setState(function(f) {
          var d = f.keyEntities.map(function(m) {
            return m.key !== p ? m : R(R({}, m), {}, {
              status: wt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var f = s.state.keyEntities, d = f.filter(function(m) {
            var y = m.status;
            return y !== wt;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Pe(i, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, u = this.props, p = u.component, f = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var m = un(u, vi), y = p || F.Fragment, w = {};
        return yi.forEach(function(h) {
          w[h] = m[h], delete m[h];
        }), delete m.keys, /* @__PURE__ */ F.createElement(y, m, c.map(function(h, b) {
          var E = h.status, C = un(h, bi), g = E === Ot || E === Ft;
          return /* @__PURE__ */ F.createElement(t, Re({}, w, {
            key: C.key,
            visible: g,
            eventProps: C,
            onVisibleChanged: function(v) {
              d == null || d(v, {
                key: C.key
              }), v || a.removeKey(C.key);
            }
          }), function(x, v) {
            return f(R(R({}, x), {}, {
              index: b
            }), v);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var u = a.keys, p = c.keyEntities, f = $t(u), d = gi(p, f);
        return {
          keyEntities: d.filter(function(m) {
            var y = p.find(function(w) {
              var h = w.key;
              return m.key === h;
            });
            return !(y && y.status === wt && m.status === At);
          })
        };
      }
    }]), i;
  }(F.Component);
  return I(n, "defaultProps", {
    component: "div"
  }), n;
}
const wi = Si(Vn);
function xi(e, t) {
  const {
    children: n,
    upload: r,
    rootClassName: o
  } = e, i = l.useRef(null);
  return l.useImperativeHandle(t, () => i.current), /* @__PURE__ */ l.createElement(Rn, Re({}, r, {
    showUploadList: !1,
    rootClassName: o,
    ref: i
  }), n);
}
const Qn = /* @__PURE__ */ l.forwardRef(xi);
var Yn = /* @__PURE__ */ Pe(function e() {
  Te(this, e);
}), Jn = "CALC_UNIT", Ei = new RegExp(Jn, "g");
function xt(e) {
  return typeof e == "number" ? "".concat(e).concat(Jn) : e;
}
var Ci = /* @__PURE__ */ function(e) {
  dt(n, e);
  var t = pt(n);
  function n(r, o) {
    var i;
    Te(this, n), i = t.call(this), I(xe(i), "result", ""), I(xe(i), "unitlessCssVar", void 0), I(xe(i), "lowPriority", void 0);
    var s = Z(r);
    return i.unitlessCssVar = o, r instanceof n ? i.result = "(".concat(r.result, ")") : s === "number" ? i.result = xt(r) : s === "string" && (i.result = r), i;
  }
  return Pe(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(xt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(xt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var i = this, s = o || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (c = !1), this.result = this.result.replace(Ei, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Yn), _i = /* @__PURE__ */ function(e) {
  dt(n, e);
  var t = pt(n);
  function n(r) {
    var o;
    return Te(this, n), o = t.call(this), I(xe(o), "result", 0), r instanceof n ? o.result = r.result : typeof r == "number" && (o.result = r), o;
  }
  return Pe(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof n ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof n ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(Yn), Li = function(t, n) {
  var r = t === "css" ? Ci : _i;
  return function(o) {
    return new r(o, n);
  };
}, bn = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function yn(e, t, n, r) {
  var o = R({}, t[e]);
  if (r != null && r.deprecatedTokens) {
    var i = r.deprecatedTokens;
    i.forEach(function(a) {
      var c = ee(a, 2), u = c[0], p = c[1];
      if (o != null && o[u] || o != null && o[p]) {
        var f;
        (f = o[p]) !== null && f !== void 0 || (o[p] = o == null ? void 0 : o[u]);
      }
    });
  }
  var s = R(R({}, n), o);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var er = typeof CSSINJS_STATISTIC < "u", kt = !0;
function Bt() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!er)
    return Object.assign.apply(Object, [{}].concat(t));
  kt = !1;
  var r = {};
  return t.forEach(function(o) {
    if (Z(o) === "object") {
      var i = Object.keys(o);
      i.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[s];
          }
        });
      });
    }
  }), kt = !0, r;
}
var Sn = {};
function Ri() {
}
var Ii = function(t) {
  var n, r = t, o = Ri;
  return er && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), r = new Proxy(t, {
    get: function(s, a) {
      if (kt) {
        var c;
        (c = n) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), o = function(s, a) {
    var c;
    Sn[s] = {
      global: Array.from(n),
      component: R(R({}, (c = Sn[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: r,
    keys: n,
    flush: o
  };
};
function wn(e, t, n) {
  if (typeof n == "function") {
    var r;
    return n(Bt(t, (r = t[e]) !== null && r !== void 0 ? r : {}));
  }
  return n ?? {};
}
function Ti(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "max(".concat(r.map(function(i) {
        return Xt(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "min(".concat(r.map(function(i) {
        return Xt(i);
      }).join(","), ")");
    }
  };
}
var Pi = 1e3 * 60 * 10, Mi = /* @__PURE__ */ function() {
  function e() {
    Te(this, e), I(this, "map", /* @__PURE__ */ new Map()), I(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), I(this, "nextID", 0), I(this, "lastAccessBeat", /* @__PURE__ */ new Map()), I(this, "accessBeat", 0);
  }
  return Pe(e, [{
    key: "set",
    value: function(n, r) {
      this.clear();
      var o = this.getCompositeKey(n);
      this.map.set(o, r), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var r = this.getCompositeKey(n), o = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var r = this, o = n.map(function(i) {
        return i && Z(i) === "object" ? "obj_".concat(r.getObjectID(i)) : "".concat(Z(i), "_").concat(i);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var r = this.nextID;
      return this.objectIDMap.set(n, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(o, i) {
          r - o > Pi && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), xn = new Mi();
function Oi(e, t) {
  return l.useMemo(function() {
    var n = xn.get(t);
    if (n)
      return n;
    var r = e();
    return xn.set(t, r), r;
  }, t);
}
var Fi = function() {
  return {};
};
function Ai(e) {
  var t = e.useCSP, n = t === void 0 ? Fi : t, r = e.useToken, o = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(d, m, y, w) {
    var h = Array.isArray(d) ? d[0] : d;
    function b(S) {
      return "".concat(String(h)).concat(S.slice(0, 1).toUpperCase()).concat(S.slice(1));
    }
    var E = (w == null ? void 0 : w.unitless) || {}, C = typeof a == "function" ? a(d) : {}, g = R(R({}, C), {}, I({}, b("zIndexPopup"), !0));
    Object.keys(E).forEach(function(S) {
      g[b(S)] = E[S];
    });
    var x = R(R({}, w), {}, {
      unitless: g,
      prefixToken: b
    }), v = p(d, m, y, x), L = u(h, y, x);
    return function(S) {
      var T = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : S, $ = v(S, T), k = ee($, 2), _ = k[1], M = L(T), P = ee(M, 2), O = P[0], j = P[1];
      return [O, _, j];
    };
  }
  function u(d, m, y) {
    var w = y.unitless, h = y.injectStyle, b = h === void 0 ? !0 : h, E = y.prefixToken, C = y.ignore, g = function(L) {
      var S = L.rootCls, T = L.cssVar, $ = T === void 0 ? {} : T, k = r(), _ = k.realToken;
      return Ar({
        path: [d],
        prefix: $.prefix,
        key: $.key,
        unitless: w,
        ignore: C,
        token: _,
        scope: S
      }, function() {
        var M = wn(d, _, m), P = yn(d, _, M, {
          deprecatedTokens: y == null ? void 0 : y.deprecatedTokens
        });
        return Object.keys(M).forEach(function(O) {
          P[E(O)] = P[O], delete P[O];
        }), P;
      }), null;
    }, x = function(L) {
      var S = r(), T = S.cssVar;
      return [function($) {
        return b && T ? /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(g, {
          rootCls: L,
          cssVar: T,
          component: d
        }), $) : $;
      }, T == null ? void 0 : T.key];
    };
    return x;
  }
  function p(d, m, y) {
    var w = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = Array.isArray(d) ? d : [d, d], b = ee(h, 1), E = b[0], C = h.join("-"), g = e.layer || {
      name: "antd"
    };
    return function(x) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : x, L = r(), S = L.theme, T = L.realToken, $ = L.hashId, k = L.token, _ = L.cssVar, M = o(), P = M.rootPrefixCls, O = M.iconPrefixCls, j = n(), H = _ ? "css" : "js", Q = Oi(function() {
        var z = /* @__PURE__ */ new Set();
        return _ && Object.keys(w.unitless || {}).forEach(function(Y) {
          z.add(gt(Y, _.prefix)), z.add(gt(Y, bn(E, _.prefix)));
        }), Li(H, z);
      }, [H, E, _ == null ? void 0 : _.prefix]), pe = Ti(H), ue = pe.max, X = pe.min, D = {
        theme: S,
        token: k,
        hashId: $,
        nonce: function() {
          return j.nonce;
        },
        clientOnly: w.clientOnly,
        layer: g,
        // antd is always at top of styles
        order: w.order || -999
      };
      typeof i == "function" && Wt(R(R({}, D), {}, {
        clientOnly: !1,
        path: ["Shared", P]
      }), function() {
        return i(k, {
          prefix: {
            rootPrefixCls: P,
            iconPrefixCls: O
          },
          csp: j
        });
      });
      var K = Wt(R(R({}, D), {}, {
        path: [C, x, O]
      }), function() {
        if (w.injectStyle === !1)
          return [];
        var z = Ii(k), Y = z.token, me = z.flush, ae = wn(E, T, y), Me = ".".concat(x), Ee = yn(E, T, ae, {
          deprecatedTokens: w.deprecatedTokens
        });
        _ && ae && Z(ae) === "object" && Object.keys(ae).forEach(function(Se) {
          ae[Se] = "var(".concat(gt(Se, bn(E, _.prefix)), ")");
        });
        var he = Bt(Y, {
          componentCls: Me,
          prefixCls: x,
          iconCls: ".".concat(O),
          antCls: ".".concat(P),
          calc: Q,
          // @ts-ignore
          max: ue,
          // @ts-ignore
          min: X
        }, _ ? ae : Ee), fe = m(he, {
          hashId: $,
          prefixCls: x,
          rootPrefixCls: P,
          iconPrefixCls: O
        });
        me(E, Ee);
        var le = typeof s == "function" ? s(he, x, v, w.resetFont) : null;
        return [w.resetStyle === !1 ? null : le, fe];
      });
      return [K, $];
    };
  }
  function f(d, m, y) {
    var w = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = p(d, m, y, R({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, w)), b = function(C) {
      var g = C.prefixCls, x = C.rootCls, v = x === void 0 ? g : x;
      return h(g, v), null;
    };
    return b;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: f,
    genComponentStyleHook: p
  };
}
const G = Math.round;
function Et(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = n.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    r[o] = t(r[o] || 0, n[o] || "", o);
  return n[3] ? r[3] = n[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const En = (e, t, n) => n === 0 ? e : e / 100;
function Ae(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class de {
  constructor(t) {
    I(this, "isValid", !0), I(this, "r", 0), I(this, "g", 0), I(this, "b", 0), I(this, "a", 1), I(this, "_h", void 0), I(this, "_s", void 0), I(this, "_l", void 0), I(this, "_v", void 0), I(this, "_max", void 0), I(this, "_min", void 0), I(this, "_brightness", void 0);
    function n(r) {
      return r[0] in t && r[1] in t && r[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(i) {
        return r.startsWith(i);
      };
      const r = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : o("rgb") ? this.fromRgbString(r) : o("hsl") ? this.fromHslString(r) : (o("hsv") || o("hsb")) && this.fromHsvString(r);
    } else if (t instanceof de)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = Ae(t.r), this.g = Ae(t.g), this.b = Ae(t.b), this.a = typeof t.a == "number" ? Ae(t.a, 1) : 1;
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
    function t(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), r = t(this.g), o = t(this.b);
    return 0.2126 * n + 0.7152 * r + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = G(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const r = this._c(t), o = n / 100, i = (a) => (r[a] - this[a]) * o + this[a], s = {
      r: G(i("r")),
      g: G(i("g")),
      b: G(i("b")),
      a: G(i("a") * 100) / 100
    };
    return this._c(s);
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
    const n = this._c(t), r = this.a + n.a * (1 - this.a), o = (i) => G((this[i] * this.a + n[i] * n.a * (1 - this.a)) / r);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: r
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
    const r = (this.g || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = G(this.a * 255).toString(16);
      t += i.length === 2 ? i : "0" + i;
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
    const t = this.getHue(), n = G(this.getSaturation() * 100), r = G(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${r}%,${this.a})` : `hsl(${t},${n}%,${r}%)`;
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
  _sc(t, n, r) {
    const o = this.clone();
    return o[t] = Ae(n, r), o;
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
    function r(o, i) {
      return parseInt(n[o] + n[i || o], 16);
    }
    n.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = n[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = n[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: r,
    a: o
  }) {
    if (this._h = t % 360, this._s = n, this._l = r, this.a = typeof o == "number" ? o : 1, n <= 0) {
      const d = G(r * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, u = (1 - Math.abs(2 * r - 1)) * n, p = u * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = u, s = p) : c >= 1 && c < 2 ? (i = p, s = u) : c >= 2 && c < 3 ? (s = u, a = p) : c >= 3 && c < 4 ? (s = p, a = u) : c >= 4 && c < 5 ? (i = p, a = u) : c >= 5 && c < 6 && (i = u, a = p);
    const f = r - u / 2;
    this.r = G((i + f) * 255), this.g = G((s + f) * 255), this.b = G((a + f) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: r,
    a: o
  }) {
    this._h = t % 360, this._s = n, this._v = r, this.a = typeof o == "number" ? o : 1;
    const i = G(r * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, u = G(r * (1 - n) * 255), p = G(r * (1 - n * c) * 255), f = G(r * (1 - n * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = u;
        break;
      case 1:
        this.r = p, this.b = u;
        break;
      case 2:
        this.r = u, this.b = f;
        break;
      case 3:
        this.r = u, this.g = p;
        break;
      case 4:
        this.r = f, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = p;
        break;
    }
  }
  fromHsvString(t) {
    const n = Et(t, En);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = Et(t, En);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = Et(t, (r, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? G(r / 100 * 255) : r
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const $i = {
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
}, ki = Object.assign(Object.assign({}, $i), {
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
function Ct(e) {
  return e >= 0 && e <= 255;
}
function Ve(e, t) {
  const {
    r: n,
    g: r,
    b: o,
    a: i
  } = new de(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new de(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const p = Math.round((n - s * (1 - u)) / u), f = Math.round((r - a * (1 - u)) / u), d = Math.round((o - c * (1 - u)) / u);
    if (Ct(p) && Ct(f) && Ct(d))
      return new de({
        r: p,
        g: f,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new de({
    r: n,
    g: r,
    b: o,
    a: 1
  }).toRgbString();
}
var ji = function(e, t) {
  var n = {};
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
    t.indexOf(r[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, r[o]) && (n[r[o]] = e[r[o]]);
  return n;
};
function Di(e) {
  const {
    override: t
  } = e, n = ji(e, ["override"]), r = Object.assign({}, t);
  Object.keys(ki).forEach((d) => {
    delete r[d];
  });
  const o = Object.assign(Object.assign({}, n), r), i = 480, s = 576, a = 768, c = 992, u = 1200, p = 1600;
  if (o.motion === !1) {
    const d = "0s";
    o.motionDurationFast = d, o.motionDurationMid = d, o.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: Ve(o.colorBorderSecondary, o.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: o.colorTextQuaternary,
    colorTextDisabled: o.colorTextQuaternary,
    colorTextHeading: o.colorText,
    colorTextLabel: o.colorTextSecondary,
    colorTextDescription: o.colorTextTertiary,
    colorTextLightSolid: o.colorWhite,
    colorHighlight: o.colorError,
    colorBgTextHover: o.colorFillSecondary,
    colorBgTextActive: o.colorFill,
    colorIcon: o.colorTextTertiary,
    colorIconHover: o.colorText,
    colorErrorOutline: Ve(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: Ve(o.colorWarningBg, o.colorBgContainer),
    // Font
    fontSizeIcon: o.fontSizeSM,
    // Line
    lineWidthFocus: o.lineWidth * 3,
    // Control
    lineWidth: o.lineWidth,
    controlOutlineWidth: o.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: o.controlHeight / 2,
    controlItemBgHover: o.colorFillTertiary,
    controlItemBgActive: o.colorPrimaryBg,
    controlItemBgActiveHover: o.colorPrimaryBgHover,
    controlItemBgActiveDisabled: o.colorFill,
    controlTmpOutline: o.colorFillQuaternary,
    controlOutline: Ve(o.colorPrimaryBg, o.colorBgContainer),
    lineType: o.lineType,
    borderRadius: o.borderRadius,
    borderRadiusXS: o.borderRadiusXS,
    borderRadiusSM: o.borderRadiusSM,
    borderRadiusLG: o.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: o.sizeXXS,
    paddingXS: o.sizeXS,
    paddingSM: o.sizeSM,
    padding: o.size,
    paddingMD: o.sizeMD,
    paddingLG: o.sizeLG,
    paddingXL: o.sizeXL,
    paddingContentHorizontalLG: o.sizeLG,
    paddingContentVerticalLG: o.sizeMS,
    paddingContentHorizontal: o.sizeMS,
    paddingContentVertical: o.sizeSM,
    paddingContentHorizontalSM: o.size,
    paddingContentVerticalSM: o.sizeXS,
    marginXXS: o.sizeXXS,
    marginXS: o.sizeXS,
    marginSM: o.sizeSM,
    margin: o.size,
    marginMD: o.sizeMD,
    marginLG: o.sizeLG,
    marginXL: o.sizeXL,
    marginXXL: o.sizeXXL,
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
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: p - 1,
    screenXXL: p,
    screenXXLMin: p,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new de("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new de("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new de("rgba(0, 0, 0, 0.09)").toRgbString()}
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
  }), r);
}
const Ni = {
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
}, zi = {
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
}, Hi = $r(je.defaultAlgorithm), Ui = {
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
}, tr = (e, t, n) => {
  const r = n.getDerivativeToken(e), {
    override: o,
    ...i
  } = t;
  let s = {
    ...r,
    override: o
  };
  return s = Di(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: u,
      ...p
    } = c;
    let f = p;
    u && (f = tr({
      ...s,
      ...p
    }, {
      override: p
    }, u)), s[a] = f;
  }), s;
};
function Bi() {
  const {
    token: e,
    hashed: t,
    theme: n = Hi,
    override: r,
    cssVar: o
  } = l.useContext(je._internalContext), [i, s, a] = kr(n, [je.defaultSeed, e], {
    salt: `${To}-${t || ""}`,
    override: r,
    getComputedToken: tr,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: Ni,
      ignore: zi,
      preserve: Ui
    }
  });
  return [n, a, t ? s : "", i, o];
}
const {
  genStyleHooks: Vi
} = Ai({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Qe();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, r, o] = Bi();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: r,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Qe();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Xi = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list-card`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [r]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${r}-name,${r}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${r}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${r}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: n(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: n(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: n(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: n(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${r}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${r}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: o,
        height: o,
        lineHeight: 1,
        [`&:not(${r}-status-error)`]: {
          border: 0
        },
        // Img
        img: {
          width: "100%",
          height: "100%",
          verticalAlign: "top",
          objectFit: "cover",
          borderRadius: "inherit"
        },
        // Mask
        [`${r}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${r}-status-error`]: {
          [`img, ${r}-img-mask`]: {
            borderRadius: n(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${r}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${r}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${r}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: e.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: e.fontSize,
        cursor: "pointer",
        opacity: e.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: e.opacityLoading
        }
      },
      [`&:hover ${r}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${r}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((i) => `${i} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: n(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, jt = {
  "&, *": {
    boxSizing: "border-box"
  }
}, Wi = (e) => {
  const {
    componentCls: t,
    calc: n,
    antCls: r
  } = e, o = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...jt,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${i}-inner`]: {
          display: "none"
        }
      },
      [i]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [i]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...jt,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
          padding: 0
        },
        [`&${i}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${i}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${i}-inner`]: {
          gap: n(e.paddingXXS).div(2).equal()
        },
        [`${i}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${i}-title${i}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${i}-description`]: {}
      }
    }
  };
}, Gi = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...jt,
      // =============================== File List ===============================
      [r]: {
        display: "flex",
        flexWrap: "wrap",
        gap: e.paddingSM,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        color: e.colorText,
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        width: "100%",
        background: e.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${e.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: n(o).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: o,
          height: o,
          fontSize: e.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: e.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&:dir(ltr)": {
          [`&${r}-overflow-ping-start ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-end ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${r}-overflow-ping-end ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-start ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, Ki = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new de(t).setA(0.85).toRgbString()
  };
}, nr = Vi("Attachments", (e) => {
  const t = Bt(e, {});
  return [Wi(t), Gi(t), Xi(t)];
}, Ki), qi = (e) => e.indexOf("image/") === 0, Xe = 200;
function Zi(e) {
  return new Promise((t) => {
    if (!e || !e.type || !qi(e.type)) {
      t("");
      return;
    }
    const n = new Image();
    if (n.onload = () => {
      const {
        width: r,
        height: o
      } = n, i = r / o, s = i > 1 ? Xe : Xe * i, a = i > 1 ? Xe / i : Xe, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(n, 0, 0, s, a);
      const p = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(n.src), t(p);
    }, n.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (n.src = r.result);
      }, r.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && t(r.result);
      }, r.readAsDataURL(e);
    } else
      n.src = window.URL.createObjectURL(e);
  });
}
function Qi() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "audio"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function Yi(e) {
  const {
    percent: t
  } = e, {
    token: n
  } = je.useToken();
  return /* @__PURE__ */ l.createElement(yr, {
    type: "circle",
    percent: t,
    size: n.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ l.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function Ji() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "video"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const _t = " ", Dt = "#8c8c8c", rr = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], es = [{
  icon: /* @__PURE__ */ l.createElement(Cr, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ l.createElement(_r, null),
  color: Dt,
  ext: rr
}, {
  icon: /* @__PURE__ */ l.createElement(Lr, null),
  color: Dt,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Rr, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ l.createElement(Ir, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Tr, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Pr, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ l.createElement(Ji, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ l.createElement(Qi, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Cn(e, t) {
  return t.some((n) => e.toLowerCase() === `.${n}`);
}
function ts(e) {
  let t = e;
  const n = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; t >= 1024 && r < n.length - 1; )
    t /= 1024, r++;
  return `${t.toFixed(0)} ${n[r]}`;
}
function ns(e, t) {
  const {
    prefixCls: n,
    item: r,
    onRemove: o,
    className: i,
    style: s,
    imageProps: a
  } = e, c = l.useContext(Ne), {
    disabled: u
  } = c || {}, {
    name: p,
    size: f,
    percent: d,
    status: m = "done",
    description: y
  } = r, {
    getPrefixCls: w
  } = Qe(), h = w("attachment", n), b = `${h}-list-card`, [E, C, g] = nr(h), [x, v] = l.useMemo(() => {
    const j = p || "", H = j.match(/^(.*)\.[^.]+$/);
    return H ? [H[1], j.slice(H[1].length)] : [j, ""];
  }, [p]), L = l.useMemo(() => Cn(v, rr), [v]), S = l.useMemo(() => y || (m === "uploading" ? `${d || 0}%` : m === "error" ? r.response || _t : f ? ts(f) : _t), [m, d]), [T, $] = l.useMemo(() => {
    for (const {
      ext: j,
      icon: H,
      color: Q
    } of es)
      if (Cn(v, j))
        return [H, Q];
    return [/* @__PURE__ */ l.createElement(xr, {
      key: "defaultIcon"
    }), Dt];
  }, [v]), [k, _] = l.useState();
  l.useEffect(() => {
    if (r.originFileObj) {
      let j = !0;
      return Zi(r.originFileObj).then((H) => {
        j && _(H);
      }), () => {
        j = !1;
      };
    }
    _(void 0);
  }, [r.originFileObj]);
  let M = null;
  const P = r.thumbUrl || r.url || k, O = L && (r.originFileObj || P);
  return O ? M = /* @__PURE__ */ l.createElement(l.Fragment, null, P && /* @__PURE__ */ l.createElement(Sr, Re({}, a, {
    alt: "preview",
    src: P
  })), m !== "done" && /* @__PURE__ */ l.createElement("div", {
    className: `${b}-img-mask`
  }, m === "uploading" && d !== void 0 && /* @__PURE__ */ l.createElement(Yi, {
    percent: d,
    prefixCls: b
  }), m === "error" && /* @__PURE__ */ l.createElement("div", {
    className: `${b}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-ellipsis-prefix`
  }, S)))) : M = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-icon`,
    style: {
      color: $
    }
  }, T), /* @__PURE__ */ l.createElement("div", {
    className: `${b}-content`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-name`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-ellipsis-prefix`
  }, x ?? _t), /* @__PURE__ */ l.createElement("div", {
    className: `${b}-ellipsis-suffix`
  }, v)), /* @__PURE__ */ l.createElement("div", {
    className: `${b}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-ellipsis-prefix`
  }, S)))), E(/* @__PURE__ */ l.createElement("div", {
    className: ie(b, {
      [`${b}-status-${m}`]: m,
      [`${b}-type-preview`]: O,
      [`${b}-type-overview`]: !O
    }, i, C, g),
    style: s,
    ref: t
  }, M, !u && o && /* @__PURE__ */ l.createElement("button", {
    type: "button",
    className: `${b}-remove`,
    onClick: () => {
      o(r);
    }
  }, /* @__PURE__ */ l.createElement(Er, null))));
}
const or = /* @__PURE__ */ l.forwardRef(ns), _n = 1;
function rs(e) {
  const {
    prefixCls: t,
    items: n,
    onRemove: r,
    overflow: o,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: u,
    imageProps: p
  } = e, f = `${t}-list`, d = l.useRef(null), [m, y] = l.useState(!1), {
    disabled: w
  } = l.useContext(Ne);
  l.useEffect(() => (y(!0), () => {
    y(!1);
  }), []);
  const [h, b] = l.useState(!1), [E, C] = l.useState(!1), g = () => {
    const S = d.current;
    S && (o === "scrollX" ? (b(Math.abs(S.scrollLeft) >= _n), C(S.scrollWidth - S.clientWidth - Math.abs(S.scrollLeft) >= _n)) : o === "scrollY" && (b(S.scrollTop !== 0), C(S.scrollHeight - S.clientHeight !== S.scrollTop)));
  };
  l.useEffect(() => {
    g();
  }, [o, n.length]);
  const x = (S) => {
    const T = d.current;
    T && T.scrollTo({
      left: T.scrollLeft + S * T.clientWidth,
      behavior: "smooth"
    });
  }, v = () => {
    x(-1);
  }, L = () => {
    x(1);
  };
  return /* @__PURE__ */ l.createElement("div", {
    className: ie(f, {
      [`${f}-overflow-${e.overflow}`]: o,
      [`${f}-overflow-ping-start`]: h,
      [`${f}-overflow-ping-end`]: E
    }, s),
    ref: d,
    onScroll: g,
    style: a
  }, /* @__PURE__ */ l.createElement(wi, {
    keys: n.map((S) => ({
      key: S.uid,
      item: S
    })),
    motionName: `${f}-card-motion`,
    component: !1,
    motionAppear: m,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: S,
    item: T,
    className: $,
    style: k
  }) => /* @__PURE__ */ l.createElement(or, {
    key: S,
    prefixCls: t,
    item: T,
    onRemove: r,
    className: ie($, c),
    imageProps: p,
    style: {
      ...k,
      ...u
    }
  })), !w && /* @__PURE__ */ l.createElement(Qn, {
    upload: i
  }, /* @__PURE__ */ l.createElement(mt, {
    className: `${f}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ l.createElement(Mr, {
    className: `${f}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(mt, {
    size: "small",
    shape: "circle",
    className: `${f}-prev-btn`,
    icon: /* @__PURE__ */ l.createElement(Or, null),
    onClick: v
  }), /* @__PURE__ */ l.createElement(mt, {
    size: "small",
    shape: "circle",
    className: `${f}-next-btn`,
    icon: /* @__PURE__ */ l.createElement(Fr, null),
    onClick: L
  })));
}
function os(e, t) {
  const {
    prefixCls: n,
    placeholder: r = {},
    upload: o,
    className: i,
    style: s
  } = e, a = `${n}-placeholder`, c = r || {}, {
    disabled: u
  } = l.useContext(Ne), [p, f] = l.useState(!1), d = () => {
    f(!0);
  }, m = (h) => {
    h.currentTarget.contains(h.relatedTarget) || f(!1);
  }, y = () => {
    f(!1);
  }, w = /* @__PURE__ */ l.isValidElement(r) ? r : /* @__PURE__ */ l.createElement(wr, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ l.createElement(ht.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ l.createElement(ht.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ l.createElement(ht.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ l.createElement("div", {
    className: ie(a, {
      [`${a}-drag-in`]: p,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: d,
    onDragLeave: m,
    onDrop: y,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ l.createElement(Rn.Dragger, Re({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), w));
}
const is = /* @__PURE__ */ l.forwardRef(os);
function ss(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    rootStyle: o,
    className: i,
    style: s,
    items: a,
    children: c,
    getDropContainer: u,
    placeholder: p,
    onChange: f,
    onRemove: d,
    overflow: m,
    imageProps: y,
    disabled: w,
    classNames: h = {},
    styles: b = {},
    ...E
  } = e, {
    getPrefixCls: C,
    direction: g
  } = Qe(), x = C("attachment", n), v = Oo("attachments"), {
    classNames: L,
    styles: S
  } = v, T = l.useRef(null), $ = l.useRef(null);
  l.useImperativeHandle(t, () => ({
    nativeElement: T.current,
    upload: (D) => {
      var z, Y;
      const K = (Y = (z = $.current) == null ? void 0 : z.nativeElement) == null ? void 0 : Y.querySelector('input[type="file"]');
      if (K) {
        const me = new DataTransfer();
        me.items.add(D), K.files = me.files, K.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [k, _, M] = nr(x), P = ie(_, M), [O, j] = Do([], {
    value: a
  }), H = Ie((D) => {
    j(D.fileList), f == null || f(D);
  }), Q = {
    ...E,
    fileList: O,
    onChange: H
  }, pe = (D) => Promise.resolve(typeof d == "function" ? d(D) : d).then((K) => {
    if (K === !1)
      return;
    const z = O.filter((Y) => Y.uid !== D.uid);
    H({
      file: {
        ...D,
        status: "removed"
      },
      fileList: z
    });
  });
  let ue;
  const X = (D, K, z) => {
    const Y = typeof p == "function" ? p(D) : p;
    return /* @__PURE__ */ l.createElement(is, {
      placeholder: Y,
      upload: Q,
      prefixCls: x,
      className: ie(L.placeholder, h.placeholder),
      style: {
        ...S.placeholder,
        ...b.placeholder,
        ...K == null ? void 0 : K.style
      },
      ref: z
    });
  };
  if (c)
    ue = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(Qn, {
      upload: Q,
      rootClassName: r,
      ref: $
    }, c), /* @__PURE__ */ l.createElement(ln, {
      getDropContainer: u,
      prefixCls: x,
      className: ie(P, r)
    }, X("drop")));
  else {
    const D = O.length > 0;
    ue = /* @__PURE__ */ l.createElement("div", {
      className: ie(x, P, {
        [`${x}-rtl`]: g === "rtl"
      }, i, r),
      style: {
        ...o,
        ...s
      },
      dir: g || "ltr",
      ref: T
    }, /* @__PURE__ */ l.createElement(rs, {
      prefixCls: x,
      items: O,
      onRemove: pe,
      overflow: m,
      upload: Q,
      listClassName: ie(L.list, h.list),
      listStyle: {
        ...S.list,
        ...b.list,
        ...!D && {
          display: "none"
        }
      },
      itemClassName: ie(L.item, h.item),
      itemStyle: {
        ...S.item,
        ...b.item
      },
      imageProps: y
    }), X("inline", D ? {
      style: {
        display: "none"
      }
    } : {}, $), /* @__PURE__ */ l.createElement(ln, {
      getDropContainer: u || (() => T.current),
      prefixCls: x,
      className: P
    }, X("drop")));
  }
  return k(/* @__PURE__ */ l.createElement(Ne.Provider, {
    value: {
      disabled: w
    }
  }, ue));
}
const ir = /* @__PURE__ */ l.forwardRef(ss);
ir.FileCard = or;
function as(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ls(e, t = !1) {
  try {
    if (hr(e))
      return e;
    if (t && !as(e))
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
function J(e, t) {
  return Je(() => ls(e, t), [e, t]);
}
function cs(e, t) {
  const n = Je(() => l.Children.toArray(e.originalChildren || e).filter((i) => i.props.node && !i.props.node.ignore && (!i.props.nodeSlotKey || t)).sort((i, s) => {
    if (i.props.node.slotIndex && s.props.node.slotIndex) {
      const a = $e(i.props.node.slotIndex) || 0, c = $e(s.props.node.slotIndex) || 0;
      return a - c === 0 && i.props.node.subSlotIndex && s.props.node.subSlotIndex ? ($e(i.props.node.subSlotIndex) || 0) - ($e(s.props.node.subSlotIndex) || 0) : a - c;
    }
    return 0;
  }).map((i) => i.props.node.target), [e, t]);
  return Co(n);
}
function us(e, t) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (n[r] = e[r]), n), {});
}
const fs = ({
  children: e,
  ...t
}) => /* @__PURE__ */ te.jsx(te.Fragment, {
  children: e(t)
});
function ds(e) {
  return l.createElement(fs, {
    children: e
  });
}
function Ln(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ds((n) => /* @__PURE__ */ te.jsx(vr, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ te.jsx(ke, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...n
    })
  })) : /* @__PURE__ */ te.jsx(ke, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function oe({
  key: e,
  slots: t,
  targets: n
}, r) {
  return t[e] ? (...o) => n ? n.map((i, s) => /* @__PURE__ */ te.jsx(l.Fragment, {
    children: Ln(i, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ te.jsx(te.Fragment, {
    children: Ln(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const ps = (e) => !!e.name;
function Lt(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const gs = xo(({
  slots: e,
  upload: t,
  showUploadList: n,
  progress: r,
  beforeUpload: o,
  customRequest: i,
  previewFile: s,
  isImageUrl: a,
  itemRender: c,
  iconRender: u,
  data: p,
  onChange: f,
  onValueChange: d,
  onRemove: m,
  items: y,
  setSlotParams: w,
  placeholder: h,
  getDropContainer: b,
  children: E,
  maxCount: C,
  imageProps: g,
  ...x
}) => {
  const v = Lt(g == null ? void 0 : g.preview), L = e["imageProps.preview.mask"] || e["imageProps.preview.closeIcon"] || e["imageProps.preview.toolbarRender"] || e["imageProps.preview.imageRender"] || (g == null ? void 0 : g.preview) !== !1, S = J(v.getContainer), T = J(v.toolbarRender), $ = J(v.imageRender), k = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof n == "object", _ = Lt(n), M = e["placeholder.title"] || e["placeholder.description"] || e["placeholder.icon"] || typeof h == "object", P = Lt(h), O = J(_.showPreviewIcon), j = J(_.showRemoveIcon), H = J(_.showDownloadIcon), {
    token: Q
  } = je.useToken(), pe = J(o), ue = J(i), X = J(r == null ? void 0 : r.format), D = J(s), K = J(a), z = J(c), Y = J(u), me = J(h, !0), ae = J(b), Me = J(p), [Ee, he] = qe(!1), [fe, le] = qe(y);
  we(() => {
    le(y);
  }, [y]);
  const Se = Je(() => {
    const B = {};
    return fe.map((U) => {
      if (!ps(U)) {
        const ne = U.uid || U.url || U.path;
        return B[ne] || (B[ne] = 0), B[ne]++, {
          ...U,
          name: U.orig_name || U.path,
          uid: U.uid || ne + "-" + B[ne],
          status: "done"
        };
      }
      return U;
    }) || [];
  }, [fe]), Oe = cs(E), Fe = x.disabled || Ee;
  return /* @__PURE__ */ te.jsxs(te.Fragment, {
    children: [/* @__PURE__ */ te.jsx("div", {
      style: {
        display: "none"
      },
      children: Oe.length > 0 ? null : E
    }), /* @__PURE__ */ te.jsx(ir, {
      ...x,
      disabled: Fe,
      imageProps: {
        ...g,
        preview: L ? us({
          ...v,
          getContainer: S,
          toolbarRender: e["imageProps.preview.toolbarRender"] ? oe({
            slots: e,
            key: "imageProps.preview.toolbarRender"
          }) : T,
          imageRender: e["imageProps.preview.imageRender"] ? oe({
            slots: e,
            key: "imageProps.preview.imageRender"
          }) : $,
          ...e["imageProps.preview.mask"] || Reflect.has(v, "mask") ? {
            mask: e["imageProps.preview.mask"] ? /* @__PURE__ */ te.jsx(ke, {
              slot: e["imageProps.preview.mask"]
            }) : v.mask
          } : {},
          closeIcon: e["imageProps.preview.closeIcon"] ? /* @__PURE__ */ te.jsx(ke, {
            slot: e["imageProps.preview.closeIcon"]
          }) : v.closeIcon
        }) : !1,
        placeholder: e["imageProps.placeholder"] ? /* @__PURE__ */ te.jsx(ke, {
          slot: e["imageProps.placeholder"]
        }) : g == null ? void 0 : g.placeholder,
        wrapperStyle: {
          width: "100%",
          height: "100%",
          ...g == null ? void 0 : g.wrapperStyle
        },
        style: {
          width: "100%",
          height: "100%",
          objectFit: "contain",
          borderRadius: Q.borderRadius,
          ...g == null ? void 0 : g.style
        }
      },
      getDropContainer: ae,
      placeholder: e.placeholder ? oe({
        slots: e,
        key: "placeholder"
      }) : M ? (...B) => {
        var U, ne, ge;
        return {
          ...P,
          icon: e["placeholder.icon"] ? (U = oe({
            slots: e,
            key: "placeholder.icon"
          })) == null ? void 0 : U(...B) : P.icon,
          title: e["placeholder.title"] ? (ne = oe({
            slots: e,
            key: "placeholder.title"
          })) == null ? void 0 : ne(...B) : P.title,
          description: e["placeholder.description"] ? (ge = oe({
            slots: e,
            key: "placeholder.description"
          })) == null ? void 0 : ge(...B) : P.description
        };
      } : me || h,
      items: Se,
      data: Me || p,
      previewFile: D,
      isImageUrl: K,
      itemRender: e.itemRender ? oe({
        slots: e,
        key: "itemRender"
      }) : z,
      iconRender: e.iconRender ? oe({
        slots: e,
        key: "iconRender"
      }) : Y,
      maxCount: C,
      onChange: async (B) => {
        try {
          const U = B.file, ne = B.fileList, ge = Se.findIndex((q) => q.uid === U.uid);
          if (ge !== -1) {
            if (Fe)
              return;
            m == null || m(U);
            const q = fe.slice();
            q.splice(ge, 1), d == null || d(q), f == null || f(q.map((W) => W.path));
          } else {
            if (pe && !await pe(U, ne) || Fe)
              return;
            he(!0);
            let q = ne.filter((N) => N.status !== "done");
            if (C === 1)
              q = q.slice(0, 1);
            else if (q.length === 0) {
              he(!1);
              return;
            } else if (typeof C == "number") {
              const N = C - fe.length;
              q = q.slice(0, N < 0 ? 0 : N);
            }
            const W = fe, V = q.map((N) => ({
              ...N,
              size: N.size,
              uid: N.uid,
              name: N.name,
              status: "uploading"
            }));
            le((N) => [...C === 1 ? [] : N, ...V]);
            const re = (await t(q.map((N) => N.originFileObj))).filter(Boolean).map((N, sr) => ({
              ...N,
              uid: V[sr].uid
            })), ve = C === 1 ? re : [...W, ...re];
            he(!1), le(ve), d == null || d(ve), f == null || f(ve.map((N) => N.path));
          }
        } catch (U) {
          console.error(U), he(!1);
        }
      },
      customRequest: ue || Xr,
      progress: r && {
        ...r,
        format: X
      },
      showUploadList: k ? {
        ..._,
        showDownloadIcon: H || _.showDownloadIcon,
        showRemoveIcon: j || _.showRemoveIcon,
        showPreviewIcon: O || _.showPreviewIcon,
        downloadIcon: e["showUploadList.downloadIcon"] ? oe({
          slots: e,
          key: "showUploadList.downloadIcon"
        }) : _.downloadIcon,
        removeIcon: e["showUploadList.removeIcon"] ? oe({
          slots: e,
          key: "showUploadList.removeIcon"
        }) : _.removeIcon,
        previewIcon: e["showUploadList.previewIcon"] ? oe({
          slots: e,
          key: "showUploadList.previewIcon"
        }) : _.previewIcon,
        extra: e["showUploadList.extra"] ? oe({
          slots: e,
          key: "showUploadList.extra"
        }) : _.extra
      } : n,
      children: Oe.length > 0 ? E : void 0
    })]
  });
});
export {
  gs as Attachments,
  gs as default
};
