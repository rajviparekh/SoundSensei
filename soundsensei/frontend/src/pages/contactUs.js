import React, { useState } from 'react';
import NavBar from "../components/navbar";
import { BgLeft } from "../components/svg";
import '../css/home.css';

const ContactUs = () => {

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        message: '',
    });

    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const name = formData.get('name');
        const email = formData.get('email');
        const message = formData.get('message');
        window.location.href = `mailto:arya.mohan@gatech.edu?subject=Contact From ${name}&body=${message}`;

        setFormData({
            name: '',
            email: '',
            message: '',
        });
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value,
        }));
    };

    return (
        <div className={"flex flex-col"}>
            <NavBar />
            <div className={"flex flex-col items-center text-white my-gap page-body content"} style={{ fontFamily: 'Lexend Peta' }}>
                <div className={"px-10 my-gap"}>
                    <h1 className={"text-3xl font-bold mb-4"}>Contact Us</h1>
                    <p>If you have any questions or feedback, feel free to reach out to us at arya.mohan@gatech.edu.</p>
                    <br></br>
                    <br></br>
                    <form className="contact-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="text"
                        name="name"
                        placeholder="Your Name"
                        className="form-input"
                        value={formData.name}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <input
                        type="email"
                        name="email"
                        placeholder="Your Email"
                        className="form-input"
                        value={formData.email}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <textarea
                        name="message"
                        placeholder="Your Message"
                        className="form-textarea"
                        value={formData.message}
                        onChange={handleChange}
                    ></textarea>
                </div>
                <div className="form-group">
                    <button type="submit" className="submit-button">Send Message</button>
                </div>
            </form>
        </div>
            </div>
            <div id={"home-animation-top"}>
                <BgLeft />
            </div>
            <div id={"home-animation-bottom"}>
                <BgLeft />
            </div>
        </div>
    );
};

export default ContactUs;

