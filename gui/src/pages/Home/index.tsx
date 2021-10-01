import "./index.scss"

const Home = () => {
    const initialMessage = `Welcome to Granblue Automation! 
    \n*************************** 
    \nInstructions\n----------------
    \nNote: The START button is disabled until the following steps are followed through.
    \n1. Please have your game window fully visible.
    \n2. Go into the Settings Page and follow the on-screen messages to guide you through setting up the bot.
    \n3. You can head back to the Home Page and click START.
    \n\n***************************`

    return (
        <div className="logOuterContainer">
            <div className="logInnerContainer">
                <p id="log">{initialMessage}</p>
            </div>
        </div>
    )
}

export default Home
