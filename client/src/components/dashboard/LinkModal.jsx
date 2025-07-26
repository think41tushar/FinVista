import React from 'react'

const LinkModal = ({setModal, url}) => {
  return (
    <div className='fixed top-0 left-0 right-0 bottom-0 bg-black/15 flex items-center justify-center z-50'>
        <div className='bg-white p-4 rounded-lg shadow-lg flex flex-col gap-4'>
            <h2 className='text-2xl font-bold font-serif'>Connect your Fi account</h2>
            <div className='text-gray-600'>
                <p>Click on the button below to connect your Fi account to FinVista</p>
                <p>After connecting come back to this page and close this modal to continue</p>
            </div>
            <div className='flex justify-end gap-4'>
                <button className='bg-blue-500 text-white px-4 py-2 rounded' onClick={() => window.open(url, '_blank')}>Connect</button>
                <button className='bg-red-500 text-white px-4 py-2 rounded' onClick={() => setModal(false)}>Close</button>
            </div>
        </div>
    </div>
  )
}

export default LinkModal