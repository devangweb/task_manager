import { capitalizeFirstLetter} from '/utils/stringHelpers';

function Header({ userdata, handleLogout }) {
    
    
    return (
        <div className="header-container">
            <header className="header">
                <h1>Task Manager</h1>
                <div className="user-info">
                <span>Welcome, {(userdata && userdata.name)?capitalizeFirstLetter(userdata.name) : "User"}</span>
                <button onClick={handleLogout} className="logout-btn">Logout</button>
                </div>
            </header>
        </div>
    )
}

export default Header