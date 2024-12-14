import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';

import axios from "axios";

const createPortfolio = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/api/create-portfolio/", {
      name: 'ilk portföy', 
    });

    console.log("Başarılı:", response.data);
  } catch (error) {
    console.error("Hata:", error.response.data);
  }
};



const Wallet = () => {
  return (
    <div>
      <h1>Wallet PAGE</h1>
      <div>
          <button className='btn btn-primary' onClick={createPortfolio}>Create Portfolio</button>
      </div>

      <div className='portfolio-div'></div>
    </div>
    

    
  )
}

export default Wallet