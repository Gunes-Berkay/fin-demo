import logo from './logo.svg';
import './App.css';
import { Routes } from 'react-router-dom';

import MainPage from './components/MainPage'
import NewsPage from './components/NewsPage'
import Wallet from './components/Wallet'
import Navbar from './components/Navbar'
import Charts from './components/Charts'
import { Router, Route } from 'react-router-dom';

function App() {
  const myWidth = 220
  return (
    <div className='App'>
      <Navbar drawerWidth={myWidth}
       content={<Routes>
        <Route path='' element={<MainPage/>}></Route>
        <Route path='/wallet' element={<Wallet/>}></Route>
        <Route path='/charts' element={<Charts/>}></Route>
        <Route path='/news' element={<NewsPage/>}></Route>
      </Routes>}
       />



    </div>
  );
}
export default App;