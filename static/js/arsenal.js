// Performance optimized Security Arsenal & Progress Bar animations
document.addEventListener('DOMContentLoaded', function() {
    let rafId;
    initSecurityArsenal();
    
    // Optimized Intersection Observer for proficiency bars
    const proficiencyObserver = new IntersectionObserver(debounce((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                requestAnimationFrame(() => {
                    animateProficiencyBar(entry.target);
                });
                proficiencyObserver.unobserve(entry.target);
            }
        });
    }, 50), {
        threshold: 0.3,
        rootMargin: '0px 0px -50px 0px'
    });
    
    const proficiencyBars = document.querySelectorAll('.proficiency-fill');
    proficiencyBars.forEach(bar => {
        proficiencyObserver.observe(bar);
    });
    
    const toolCards = document.querySelectorAll('.tool-card');
    toolCards.forEach((card, index) => {
        card.style.animationDelay = `${Math.min(index * 0.1, 1)}s`;
        
        card.addEventListener('mouseenter', function() {
            this.style.willChange = 'transform, box-shadow';
            const proficiencyFill = this.querySelector('.proficiency-fill');
            if (proficiencyFill) {
                proficiencyFill.style.transform = 'scaleX(1.02)';
            }
        }, { passive: true });
        
        card.addEventListener('mouseleave', function() {
            this.style.willChange = 'auto';
            const proficiencyFill = this.querySelector('.proficiency-fill');
            if (proficiencyFill) {
                proficiencyFill.style.transform = 'scaleX(1)';
            }
        }, { passive: true });
        
        card.addEventListener('click', debounce(function() {
            this.classList.toggle('active');
        }, 200), { passive: true });
    });
    
    window.addEventListener('beforeunload', () => {
        if (rafId) cancelAnimationFrame(rafId);
        proficiencyObserver.disconnect();
    });
});

function initSecurityArsenal() {
    const categories = document.querySelectorAll('.arsenal-category');
    categories.forEach((category, index) => {
        category.style.animationDelay = `${index * 0.2}s`;
    });
}

function animateProficiencyBar(proficiencyFill) {
    const percentage = parseInt(proficiencyFill.dataset.percentage) || 80;
    const duration = 1500;
    let startTime = null;
    
    function animate(currentTime) {
        if (!startTime) startTime = currentTime;
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const easedProgress = easeOutQuart(progress);
        const currentPercentage = easedProgress * percentage;
        
        proficiencyFill.style.width = `${currentPercentage}%`;
        
        if (Math.floor(progress * 20) % 2 === 0) {
            const proficiencyText = proficiencyFill.parentElement.nextElementSibling;
            if (proficiencyText && proficiencyText.classList.contains('proficiency-text')) {
                const levelText = getSkillLevel(currentPercentage);
                proficiencyText.innerHTML = `▶ ${Math.round(currentPercentage)}% ${levelText}`;
            }
        }
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            proficiencyFill.style.boxShadow = `0 0 10px var(--tool-color, var(--primary-color))`;
            setTimeout(() => {
                proficiencyFill.style.boxShadow = 'none';
            }, 800);
        }
    }
    
    requestAnimationFrame(animate);
}

function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
}

function getSkillLevel(percentage) {
    if (percentage >= 90) return 'Expert';
    if (percentage >= 80) return 'Advanced';
    if (percentage >= 70) return 'Intermediate';
    if (percentage >= 60) return 'Competent';
    return 'Beginner';
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
