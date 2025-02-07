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
            <div className={footerStyles.footerTop}>
                <div id="footer-resources" className={footerStyles.column}>
                    <Link href="#footer-resources"><h3>Resources</h3></Link>
                    <ul>
                        <li><a href="https://github.com/upayanmazumder/upayan.dev" target="_blank">Source Code</a></li>
                        <li><Link href="/p/privacy-policy">Privacy Policy</Link></li>
                        <li><Link href="/p/terms-of-service">Terms of Service</Link></li>
                    </ul>
                </div>
                <div id="footer-companies" className={footerStyles.column}>
                    <Link href="#footer-companies"><h3>Companies</h3></Link>
                    <ul>
                        <li><a href="https://bbn.one" target="_blank">BBN</a></li>
                        <li><a href="https://eranodes.com" target="_blank">EraNodes</a></li>
                        <li><a href="https://purbyte.com" target="_blank">Purbyte</a></li>
                    </ul>
                </div>
                <div id="footer-projects" className={footerStyles.column}>
                    <Link href="#footer-projects"><h3>Projects</h3></Link>
                    <ul>
                        <li><a href="https://www.boardly.in/" target="_blank">Boardly</a></li>
                        <li><a href="https://github.com/upayanmazumder/Collaborative-Article-Sharing" target="_blank">Collaborative Article Sharing</a></li>
                        <li><a href="https://github.com/upayanmazumder/Status-Page" target="_blank">Status Page</a></li>
                    </ul>
                </div>
            </div>
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
