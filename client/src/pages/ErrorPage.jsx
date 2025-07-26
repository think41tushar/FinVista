import React from 'react'

const ErrorPage = () => {
  return (
    <div 
      className='w-full h-[calc(100vh-64px)] flex flex-col items-center justify-center'
      style={{ backgroundColor: 'var(--color-bg-primary)' }}
    >
        <h1 className='text-6xl font-bold' style={{ color: 'var(--color-accent)' }}>404</h1>
        <p className='text-2xl font-bold' style={{ color: 'var(--color-white)' }}>Page Not Found</p>
    </div>
  )
}

export default ErrorPage