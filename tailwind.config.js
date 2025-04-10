module.exports = {
    content: [
        './static/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#6b46c1',
                    100: '#f3effb',
                    200: '#e9e0f8',
                    300: '#d4c2f2',
                    400: '#b69ce7',
                    500: '#8a68d5',
                    600: '#6b46c1', // 主要紫色
                    700: '#553c9a', // 更深的紫色
                    800: '#44317c',
                    900: '#382967',
                },
                secondary: '#553c9a', // 更深的紫色
                accent: {
                    DEFAULT: '#f6ad55',
                    100: '#fff8f0',
                    200: '#feeed9',
                    300: '#fddcb3',
                    400: '#f9c78d',
                    500: '#f6ad55', // 温暖的橙色
                    600: '#e08e2d',
                    700: '#c47823',
                    800: '#9f621c',
                    900: '#805018',
                },
                text: '#2d3748',      // 文本颜色
                'light-color': '#f8f9fa',
                'light-gray': '#edf2f7',
                'dark-color': '#1a202c',
                success: {
                    DEFAULT: '#48bb78',
                    100: '#effcf4',
                    200: '#dff8e8',
                    300: '#b6ecc6',
                    400: '#7bdea3',
                    500: '#48bb78', // 成功绿
                    600: '#359b5e',
                    700: '#2c804d',
                    800: '#22673e',
                    900: '#19512f',
                },
            },
            boxShadow: {
                'sm': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                'md': '0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)',
                'lg': '0 10px 25px rgba(0, 0, 0, 0.1), 0 5px 10px rgba(0, 0, 0, 0.05)',
                'hover': '0 10px 25px rgba(107, 70, 193, 0.2)',
                'card': '0 3px 10px rgba(0, 0, 0, 0.08)',
            },
            borderRadius: {
                'DEFAULT': '10px',
                'xl': '1rem',
                '2xl': '1.5rem',
            },
            transitionProperty: {
                'DEFAULT': 'all',
            },
            transitionTimingFunction: {
                'DEFAULT': 'cubic-bezier(0.25, 0.8, 0.25, 1)',
                'bounce': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
            },
            transitionDuration: {
                'DEFAULT': '300ms',
            },
            animation: {
                'float': 'float 6s ease-in-out infinite',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'fadeIn': 'fadeIn 0.5s ease-in-out',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-20px)' }
                },
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' }
                }
            },
        },
    },
    plugins: [],
}
