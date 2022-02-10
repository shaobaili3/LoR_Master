import { computePosition, flip, offset } from "@floating-ui/dom"

const TooltipDirective = {
  created(el, binding) {
    const gap = binding.value.gap ? binding.value.gap : 8
    const tag = binding.value.tag ? binding.value.tag : "div"
    const classList = binding.value.class ? binding.value.class : "p-2 px-3 bg-gray-900 text-white rounded-md shadow-md shadow-black"

    var floatDom = document.createElement(tag)
    floatDom.innerText = binding.value.content
    floatDom.classList = classList

    floatDom.classList.add("opacity-0")
    floatDom.classList.add("absolute")
    floatDom.classList.add("transition-opacity")
    floatDom.classList.add("z-100")
    floatDom.classList.add("pointer-events-none")
    el.appendChild(floatDom)

    const repositionFloat = () => {
      computePosition(el, floatDom, {
        placement: "top",
        middleware: [offset(gap), flip()],
      }).then(({ x, y }) => {
        // console.log(x, y)
        Object.assign(floatDom.style, {
          left: `${x}px`,
          top: `${y}px`,
        })
      })
    }

    // Handle resize
    new ResizeObserver(repositionFloat).observe(floatDom)

    el.addEventListener("mouseenter", () => {
      repositionFloat()
      floatDom.classList.remove("opacity-0")
      floatDom.classList.add("opacity-100")
    })
    el.addEventListener("mouseleave", () => {
      floatDom.classList.remove("opacity-100")
      floatDom.classList.add("opacity-0")
    })

    repositionFloat()
  },
}

export default TooltipDirective
