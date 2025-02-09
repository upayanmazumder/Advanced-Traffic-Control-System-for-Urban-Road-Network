"use client";

import React, { JSX } from "react";
import Link from "next/link";
import footerStyles from "./footer.module.css";
import links from "../../data/links.json";
import { FaGithub, FaDiscord, FaInstagram, FaFacebook, FaLinkedin, FaArrowUp } from "react-icons/fa";

const whitelist = ["Github", "Discord", "Instagram", "Facebook", "LinkedIn"];

const iconDictionary: { [key: string]: JSX.Element } = {
    Github: <FaGithub />,
    Discord: <FaDiscord />,
    Instagram: <FaInstagram />,
    Facebook: <FaFacebook />,
    LinkedIn: <FaLinkedin />
};

const Footer: React.FC = () => {
    const filteredLinks = links.filter(link => whitelist.includes(link.name));

    return (
        <footer className={footerStyles.footer}>
            <div className={footerStyles.footerBottom}>
                <ul className={footerStyles.footerLinks}>
                    {filteredLinks.map((link, index) => (
                        <a key={index} href={link.url} target="_blank" rel="noopener">
                            {iconDictionary[link.name]}
                        </a>
                    ))}
                </ul>
                <ul className={footerStyles.toTop}>
                    <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
                        <FaArrowUp />
                    </button>
                </ul>
            </div>
        </footer>
    );
};

export default Footer;
