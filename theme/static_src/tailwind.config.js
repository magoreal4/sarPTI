module.exports = {
    content: [
        '../../templates/*.html',
        '../../templates/**/*.html', 
        '../../main/src/index-main.js',
        '../../**/templates/*.html',  
        '!../../**/node_modules',
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                'primary': '#ea3323',
                'secondary': '#2c3840',
            },
            fontFamily: {
                'roboto': ['"Roboto"', 'sans-serif']
            },
            // backgroundImage: {
            //   'fondoscz': "url('./static/img/fotoCristo1.webp')",
            //   'fondosvg': "url('./static/img/fotoCristo2.svg')",
            // },
            height: {
                'screen80': '80vh',
                'screen90': '90vh',
            },
            animation: {
                "bounce-bottom": "bounce-bottom 4s ease 2s infinite both",
                "titulo": "titulo 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) 2s  both",
                "wapp": "wapp 2s cubic-bezier(0.075, 0.820, 0.165, 1.000)   both"
            },
            keyframes: {
                "wapp": {
                    "0%": {
                        transform: "translateY(-1000px)",
                        opacity: "0"
                    },
                    to: {
                        transform: "translateY(0)",
                        opacity: "1"
                    }
                },
                "titulo": {
                    "0%": {
                        transform: "scale(0)",
                        opacity: "0"
                    },
                    to: {
                        transform: "scale(1)",
                        transform: "translate(-50%, 0)",
                        opacity: "1"
                    }
                },
                "bounce-bottom": {
                    "0%": {},
                    "40%": {
                        transform: "translateY(24px)",
                        "animation-timing-function": "ease-in"
                    },
                    "65%": {
                        transform: "translateY(12px)",
                        "animation-timing-function": "ease-in"
                    },
                    "82%": {
                        transform: "translateY(6px)",
                        "animation-timing-function": "ease-in"
                    },
                    "93%": {
                        transform: "translateY(4px)",
                        "animation-timing-function": "ease-in"
                    },
                    "25%,55%,75%,87%": {
                        transform: "translateY(0)",
                        "animation-timing-function": "ease-out"
                    },
                    to: {
                        transform: "translateY(0)",
                        "animation-timing-function": "ease-out",

                    }
                }
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
