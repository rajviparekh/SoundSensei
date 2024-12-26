import logoImage from '../media/logo-transparent.png';
import '../css/logo.css';
import { useNavigate } from 'react-router-dom';

const Logo = ({refresh}) => {
    const navigate = useNavigate();

    return (
        <div className={"w-full"} id={"navbar-logo"}>
            <img src={logoImage} height={200} width={200} className={"cursor-pointer"} onClick={() => {navigate('/')}}/>
        </div>
    )

}

export default Logo;