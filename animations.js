// GSAP Animations
gsap.registerPlugin(ScrollTrigger);

// Side Navigation Animation
gsap.from('.side-nav', {
    duration: 1,
    x: -280,
    ease: 'power3.out'
});

gsap.from('.profile-image', {
    duration: 0.8,
    scale: 0,
    opacity: 0,
    delay: 0.5,
    ease: 'back.out(1.7)'
});

gsap.from('.nav-profile h3', {
    duration: 0.8,
    y: 20,
    opacity: 0,
    delay: 0.7,
    ease: 'power2.out'
});

gsap.from('.nav-links li', {
    duration: 0.5,
    x: -50,
    opacity: 0,
    stagger: 0.1,
    delay: 0.8,
    ease: 'power2.out'
});

gsap.from('.social-links a', {
    duration: 0.5,
    y: 20,
    opacity: 0,
    stagger: 0.1,
    delay: 1.2,
    ease: 'power2.out'
});

// Sections Animation
gsap.utils.toArray('.section-container').forEach(section => {
    gsap.from(section, {
        scrollTrigger: {
            trigger: section,
            start: 'top 80%',
            end: 'top 20%',
            toggleActions: 'play none none reverse'
        },
        duration: 1,
        y: 50,
        opacity: 0,
        ease: 'power3.out'
    });
});

// Timeline Items Animation
gsap.utils.toArray('.timeline-item').forEach((item, i) => {
    gsap.from(item, {
        scrollTrigger: {
            trigger: item,
            start: 'top 85%'
        },
        duration: 0.8,
        x: -100,
        opacity: 0,
        delay: i * 0.2,
        ease: 'power2.out'
    });
});

// Skills Animation
gsap.utils.toArray('.skill-item').forEach((skill, i) => {
    const tl = gsap.timeline({
        scrollTrigger: {
            trigger: skill,
            start: 'top 85%'
        }
    });

    tl.from(skill, {
        duration: 0.6,
        y: 30,
        opacity: 0,
        ease: 'power2.out'
    })
    .from(skill.querySelector('.skill-progress-bar'), {
        duration: 1,
        width: 0,
        ease: 'power2.out'
    }, '-=0.3');
});

// Education Cards Animation
gsap.utils.toArray('.education-card').forEach((card, i) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: 'top 85%'
        },
        duration: 0.8,
        y: 50,
        opacity: 0,
        delay: i * 0.2,
        ease: 'power2.out'
    });
});

// Project Cards Animation
gsap.utils.toArray('.project-card').forEach((card, i) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: 'top 85%'
        },
        duration: 0.8,
        y: 50,
        opacity: 0,
        delay: i * 0.2,
        ease: 'power2.out'
    });
});

// Certification Cards Animation
gsap.utils.toArray('.certification-card').forEach((card, i) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: 'top 85%'
        },
        duration: 0.8,
        y: 50,
        opacity: 0,
        delay: i * 0.2,
        ease: 'power2.out'
    });
});

// Smooth Scrolling for Navigation Links
document.querySelectorAll('.nav-links a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            const headerOffset = 20;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});