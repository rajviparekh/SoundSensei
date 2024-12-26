import logoImage from '../media/logo-invert.png';
import { useNavigate } from 'react-router-dom';
import '../css/navbar.css';

const NavBar = () => {
    const navigate = useNavigate();
    return (
        <div>
            <nav className="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600">
                <div className="flex flex-wrap items-center justify-start mx-auto p-2"> 
                    <div className="flex items-center space-x-3">
                        <img src={logoImage} height={65} width={65} className="cursor-pointer" onClick={() => {navigate('/')}}/>
                    </div>
                    <ul className="flex flex-col p-2 mt-2 font-medium border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
                        <li className="md:mr-10"> 
                            <a onClick={() => {navigate('/')}} className="block py-1 px-2 text-gray-900 rounded navbar-style">Home</a>
                        </li>
                        <li className="md:mr-10"> 
                            <a onClick={() => {navigate('/about')}} className="block py-1 px-2 text-gray-900 rounded navbar-style">About</a>
                        </li>
                        <li>
                            <a onClick={() => {navigate('/contact')}} className="block py-1 px-2 text-gray-900 rounded navbar-style">Contact Us</a>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    );
}

export default NavBar;
