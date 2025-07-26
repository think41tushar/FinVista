import React, {useState, useEffect} from 'react'
import axios from 'axios'
import LinkModal from './LinkModal'
import fiLogo from "../../assets/fi-logo.png"
import { BASE_URL } from '../../utils/settings'
import { useNavigate } from 'react-router-dom'

const ConnectFiCard = () => {

    const navigate = useNavigate()
    const [loading, setLoading] = useState(false)
    const [url, setUrl] = useState("")
    const [modal, setModal] = useState(false)
    const [status, setStatus] = useState("Connect to Fi")

    useEffect(() => {
        getStatus()
    }, [loading, url])

    const checkTxnsArray = (responseText) => {
        if (typeof responseText !== 'string' || responseText.trim() === '') {
          return false;
        }
    
        const txnsArrayRegex = /"txns":\s*\[.*?\]/;
    
        if (txnsArrayRegex.test(responseText)) {
          return true
        } else {
          return false
        }
    
      }

    function extractLoginUrl(responseText) {
        const regex = /https:\/\/fi\.money\/wealth-mcp-login\?token=[^\s\\"]+/;
        const match = responseText.match(regex);
        return match ? decodeURIComponent(match[0]) : null;
    }

    const handleFiClick = async () => {
        setLoading(true)
        try{
            const response = await axios.post(`${BASE_URL}/ai/run-initial-pipeline`)
            const loginUrl = extractLoginUrl(response.data.result);
            const hasTxnsArray = checkTxnsArray(response.data.result)
            if(loginUrl){
                setUrl(loginUrl)
                setModal(true)
            }
            if(hasTxnsArray){
                navigate('/transactions')
            }
            
        }
        catch(err){
            console.log(err)
        }
        setLoading(false)
    }

    const getStatus = () =>{
        if(loading && url){
            setStatus("Analyzing...")
        }
        if(loading){
            setStatus("Connecting to Fi...")
        }
        else if(url){
            setStatus("Analyze")
        }
        else{
            setStatus("Connect to Fi")
        }
    }

  return (
    <div className='flex flex-col items-center w-full'>
        <div className='flex justify-between items-center w-full gap-4'>
            <img src={fiLogo} alt="Fi Logo" className='w-20 h-20' />
            <div className='w-[320px] text-end px-4'>
                <button className='text-2xl font-bold cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed' onClick={handleFiClick} disabled={loading}>{status}</button>
            </div>
        </div>

        {modal && <LinkModal url={url} setModal={setModal}/>}
    </div>
  )
}

export default ConnectFiCard