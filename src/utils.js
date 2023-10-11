const COLORS = {}

export function generate_color(n) {
    return `hsl(${n * 60 % 360}deg,90%,30%)`
}

export function get_stroke(name) {
    if(!COLORS[name]) COLORS[name] = generate_color(Object.keys(COLORS).length)
    return COLORS[name]
}

export function compute_path(path) {
    return path?.filter(p=>p.length===2 && !isNaN(p?.[0] + p?.[1])).map(([x,y],i)=>`${i===0 ? "M" : "L"}${x} ${y}`)?.join("")
}