<script>
import { ref, h, withDirectives, onMounted, onUpdated, Teleport } from "vue"

const logDom = {
  mounted(el, value) {
    console.log(el)
    console.log(value.value.value) // ref -> floatRef -> Dom
  },
}

import { computePosition, flip, autoPlacement, shift } from "@floating-ui/dom"

export default {
  props: {
    placement: {
      type: String,
      default: "top",
    },
    allowedPlacements: {
      type: Array,
      default: () => ["top", "bottom"],
    },
  },
  setup(props, { attrs, slots }) {
    const count = ref(1)

    var slotItem = h("div", slots.default())

    const baseRef = ref(null)
    const floatRef = ref(null)

    const isFloatShown = ref(false)

    const showFloat = () => {
      // floatRef.value.classList.remove("invisible")
      // floatRef.value.classList.add("visible")
      isFloatShown.value = true
    }

    const hideFloat = () => {
      // floatRef.value.classList.remove("visible")
      // floatRef.value.classList.add("invisible")
      isFloatShown.value = false
    }

    const repositionFloat = () => {
      computePosition(baseRef.value, floatRef.value, {
        strategy: "fixed",
        placement: props.placement,
        middleware: [autoPlacement({ allowedPlacements: props.allowedPlacements }), shift()],
      }).then(({ x, y, placement }) => {
        // console.log(floatRef.value)
        // console.log(x, y)
        Object.assign(floatRef.value.style, {
          left: `${x}px`,
          top: `${y}px`,
        })
      })
    }

    onMounted(() => {
      repositionFloat()
    })

    onUpdated(() => {
      repositionFloat()
    })

    // return the render function
    // return () => h("div", props, [props.msg + count.value, slotItem])
    // return () => [...slots.default(), h("div", attrs, "123")]
    // https://vuejs.org/api/render-function.html#withdirectives
    // [Directive, value, argument, modifier]
    // return () => [withDirectives(slots.default()[0], [[logDom, floatRef]]), h(slots.float()[0], { ref: (el) => (floatRef.value = el) })]

    return () => [
      h(slots.default()[0], {
        ref: (el) => (baseRef.value = el),
        onMouseenter: showFloat,
        onMouseleave: hideFloat,
      }),
      // h(
      //   Teleport,
      //   {
      //     to: "body",
      //   },
      //   h(slots.float({ visible: isFloatShown.value })[0], {
      //     style: "position:fixed;",
      //     ref: (el) => (floatRef.value = el),
      //   })
      // ),
      h(slots.float({ visible: isFloatShown.value })[0], {
        style: "position:fixed;",
        ref: (el) => (floatRef.value = el),
      }),
    ]
  },
}
</script>
