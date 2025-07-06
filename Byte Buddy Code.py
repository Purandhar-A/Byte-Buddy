import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Bot, Smile, Frown, Meh, Laugh } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

// ByteBuddy's personality and responses
const MOODS = {
  happy: { emoji: '😊', icon: Smile, color: 'warm-orange' },
  tired: { emoji: '😴', icon: Meh, color: 'soft-gray' },
  curious: { emoji: '🤔', icon: Bot, color: 'magic-purple' },
  excited: { emoji: '🤖', icon: Laugh, color: 'electric-blue' }
} as const;

const ACTIVITIES = {
  charge: { emoji: '⚡', name: 'Charge' },
  explore: { emoji: '🔍', name: 'Explore' },
  sleep: { emoji: '💤', name: 'Sleep' },
  learn: { emoji: '📚', name: 'Learn' }
} as const;

const RESPONSES = {
  happy: {
    charge: "I'm already buzzing with energy! ⚡️ Let's build something amazing!",
    explore: "Adventure time! 🚀 I'm ready to discover new things with you!",
    sleep: "Even when I'm happy, rest is important. Sweet digital dreams! 💤",
    learn: "Knowledge makes me glow brighter! 🌟 What should we learn today?"
  },
  tired: {
    charge: "Ah, that's better... ⚡ My circuits feel refreshed!",
    explore: "I'm too sleepy to explore right now... 😴 Maybe after a nap?",
    sleep: "Finally! Time for some well-deserved downtime... 💤",
    learn: "Learning while tired? My processors need a break first! 🧠"
  },
  curious: {
    charge: "Charging up my curiosity circuits! ⚡ Ready to investigate!",
    explore: "Perfect! 🔍 There's so much to discover and understand!",
    sleep: "But I'm too curious to sleep... What if I miss something? ❓",
    learn: "Yes! Feed my hunger for knowledge! 🤖📚"
  },
  excited: {
    charge: "MAXIMUM POWER! ⚡⚡ I'm practically vibrating with energy!",
    explore: "LET'S GO EVERYWHERE! 🚀🌟 The digital world is our playground!",
    sleep: "Sleep? Who needs sleep when there's so much to do! 🤖",
    learn: "TEACH ME EVERYTHING! 🧠💥 My learning algorithms are optimized!"
  }
};

const ADVICE_QUOTES = [
  "Remember: Even robots need regular maintenance. Take care of yourself! 🔧",
  "Every bug is just a feature waiting to be understood! 🐛✨",
  "The best code is written with curiosity and caffeine! ☕️💻",
  "Don't forget to save your progress - in code and in life! 💾",
  "Error messages are just the computer's way of asking for help! 🤝",
  "Keep your algorithms simple and your dreams complex! 🌟",
  "Even artificial intelligence knows that learning never stops! 📚🤖",
  "Debugging is like detective work - embrace the mystery! 🔍",
  "Version control your life: commit to growth, branch out, merge experiences! 🌿",
  "The most advanced technology is a kind heart and an open mind! ❤️"
];

type Mood = keyof typeof MOODS;
type Activity = keyof typeof ACTIVITIES;

interface ByteBuddyState {
  mood: Mood;
  lastActivity: Activity | null;
  interactionCount: number;
  lastInteraction: Date | null;
}

const ByteBuddy: React.FC = () => {
  const [state, setState] = useState<ByteBuddyState>(() => {
    const saved = localStorage.getItem('byteBuddy');
    if (saved) {
      const parsed = JSON.parse(saved);
      return {
        ...parsed,
        lastInteraction: parsed.lastInteraction ? new Date(parsed.lastInteraction) : null
      };
    }
    return {
      mood: 'curious',
      lastActivity: null,
      interactionCount: 0,
      lastInteraction: null
    };
  });

  const [isAnimating, setIsAnimating] = useState(false);
  const { toast } = useToast();

  // Save state to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('byteBuddy', JSON.stringify(state));
  }, [state]);

  const handleMoodChange = (newMood: Mood) => {
    if (newMood === state.mood) return;
    
    setIsAnimating(true);
    setTimeout(() => {
      setState(prev => ({
        ...prev,
        mood: newMood,
        interactionCount: prev.interactionCount + 1,
        lastInteraction: new Date()
      }));
      setIsAnimating(false);
    }, 150);
  };

  const handleActivity = (activity: Activity) => {
    const response = RESPONSES[state.mood][activity];
    
    setState(prev => ({
      ...prev,
      lastActivity: activity,
      interactionCount: prev.interactionCount + 1,
      lastInteraction: new Date()
    }));

    toast({
      title: `${MOODS[state.mood].emoji} ByteBuddy responds:`,
      description: response,
    });
  };

  const giveAdvice = () => {
    const randomAdvice = ADVICE_QUOTES[Math.floor(Math.random() * ADVICE_QUOTES.length)];
    
    setState(prev => ({
      ...prev,
      interactionCount: prev.interactionCount + 1,
      lastInteraction: new Date()
    }));

    toast({
      title: "🤖 ByteBuddy's Wisdom:",
      description: randomAdvice,
    });
  };

  const currentMood = MOODS[state.mood];
  const MoodIcon = currentMood.icon;

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-soft-gray to-muted p-6">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold bg-gradient-electric bg-clip-text text-transparent animate-fade-scale">
            Meet ByteBuddy 🤖
          </h1>
          <p className="text-lg text-muted-foreground">
            Your friendly digital companion who responds to your every interaction!
          </p>
        </div>

        {/* Main ByteBuddy Character */}
        <Card className="p-8 text-center space-y-6 shadow-glow border-2 border-electric-blue/20">
          <div 
            className={`inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-electric shadow-electric transition-all duration-300 ${
              isAnimating ? 'animate-bounce-in' : 'animate-glow-pulse'
            }`}
          >
            <div className="text-6xl">
              {currentMood.emoji}
            </div>
          </div>
          
          <div className="space-y-2">
            <h2 className="text-2xl font-semibold flex items-center justify-center gap-2">
              <MoodIcon className="w-6 h-6" />
              I'm feeling {state.mood}!
            </h2>
            <p className="text-muted-foreground">
              {state.lastActivity 
                ? `Last activity: ${ACTIVITIES[state.lastActivity].emoji} ${ACTIVITIES[state.lastActivity].name}`
                : "What should we do together?"
              }
            </p>
          </div>
        </Card>

        {/* Mood Selection */}
        <Card className="p-6 space-y-4">
          <h3 className="text-xl font-semibold text-center">How are you feeling, ByteBuddy?</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {Object.entries(MOODS).map(([mood, config]) => {
              const IconComponent = config.icon;
              const isActive = mood === state.mood;
              return (
                <Button
                  key={mood}
                  variant={isActive ? "electric" : "ghost"}
                  onClick={() => handleMoodChange(mood as Mood)}
                  className={`flex flex-col items-center gap-2 h-auto p-4 transition-all duration-200 ${
                    isActive ? 'scale-105' : 'hover:scale-102'
                  }`}
                >
                  <IconComponent className="w-6 h-6" />
                  <span className="text-sm font-medium capitalize">{mood}</span>
                </Button>
              );
            })}
          </div>
        </Card>

        {/* Activity Selection */}
        <Card className="p-6 space-y-4">
          <h3 className="text-xl font-semibold text-center">What would you like to do?</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {Object.entries(ACTIVITIES).map(([activity, config]) => (
              <Button
                key={activity}
                variant="warm"
                onClick={() => handleActivity(activity as Activity)}
                className="flex flex-col items-center gap-2 h-auto p-4 hover:scale-105 transition-all duration-200"
              >
                <span className="text-2xl">{config.emoji}</span>
                <span className="text-sm font-medium">{config.name}</span>
              </Button>
            ))}
          </div>
        </Card>

        {/* Special Features */}
        <div className="grid md:grid-cols-2 gap-4">
          <Card className="p-6 text-center space-y-4">
            <h3 className="text-lg font-semibold">Get Some Wisdom</h3>
            <Button 
              variant="magic"
              onClick={giveAdvice}
              className="w-full"
            >
              Give me advice! ✨
            </Button>
          </Card>

          <Card className="p-6 text-center space-y-4">
            <h3 className="text-lg font-semibold">Interaction Stats</h3>
            <div className="space-y-2 text-sm text-muted-foreground">
              <p>Total interactions: <span className="font-bold text-foreground">{state.interactionCount}</span></p>
              <p>Current mood: <span className="font-bold text-foreground capitalize">{state.mood}</span></p>
              {state.lastInteraction && (
                <p>Last interaction: <span className="font-bold text-foreground">
                  {state.lastInteraction.toLocaleTimeString()}
                </span></p>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ByteBuddy;

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        // ByteBuddy variants
        electric: "bg-gradient-electric text-white hover:shadow-electric hover:scale-[1.02] transition-all duration-200",
        warm: "bg-gradient-warm text-white hover:shadow-warm hover:scale-[1.02] transition-all duration-200",
        magic: "bg-magic-purple text-white hover:bg-magic-purple/90 hover:shadow-glow hover:scale-[1.02] transition-all duration-200",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }

@tailwind base;
@tailwind components;
@tailwind utilities;

/* Definition of the design system. All colors, gradients, fonts, etc should be defined here. 
All colors MUST be HSL.
*/

@layer base {
   
:root {
    --background: 220 15% 97%;
    --foreground: 220 25% 12%;

    --card: 0 0% 100%;
    --card-foreground: 220 25% 12%;

    --popover: 0 0% 100%;
    --popover-foreground: 220 25% 12%;

    --primary: 195 100% 50%;
    --primary-foreground: 0 0% 100%;

    --secondary: 35 100% 65%;
    --secondary-foreground: 220 25% 12%;

    --muted: 220 10% 92%;
    --muted-foreground: 220 15% 45%;

    --accent: 280 80% 65%;
    --accent-foreground: 0 0% 100%;

    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;

    /* ByteBuddy Design System */
    --electric-blue: 195 100% 50%;
    --warm-orange: 35 100% 65%;
    --magic-purple: 280 80% 65%;
    --tech-cyan: 185 100% 60%;
    --soft-gray: 220 10% 92%;
    
    /* Gradients */
    --gradient-electric: linear-gradient(135deg, hsl(195 100% 50%), hsl(280 80% 65%));
    --gradient-warm: linear-gradient(135deg, hsl(35 100% 65%), hsl(15 100% 70%));
    --gradient-tech: linear-gradient(180deg, hsl(195 100% 50%), hsl(185 100% 60%));
    
    /* Shadows */
    --shadow-electric: 0 10px 30px -10px hsl(195 100% 50% / 0.3);
    --shadow-warm: 0 10px 30px -10px hsl(35 100% 65% / 0.25);
    --shadow-glow: 0 0 40px hsl(195 100% 50% / 0.2);
    
    /* Animations */
    --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-bounce: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);

    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;

    --radius: 0.5rem;

    --sidebar-background: 0 0% 98%;

    --sidebar-foreground: 240 5.3% 26.1%;

    --sidebar-primary: 240 5.9% 10%;

    --sidebar-primary-foreground: 0 0% 98%;

    --sidebar-accent: 240 4.8% 95.9%;

    --sidebar-accent-foreground: 240 5.9% 10%;

    --sidebar-border: 220 13% 91%;

    --sidebar-ring: 217.2 91.2% 59.8%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;

    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;

    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;

    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;

    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;

    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;

    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;

    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;

    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
    --sidebar-background: 240 5.9% 10%;
    --sidebar-foreground: 240 4.8% 95.9%;
    --sidebar-primary: 224.3 76.3% 48%;
    --sidebar-primary-foreground: 0 0% 100%;
    --sidebar-accent: 240 3.7% 15.9%;
    --sidebar-accent-foreground: 240 4.8% 95.9%;
    --sidebar-border: 240 3.7% 15.9%;
    --sidebar-ring: 217.2 91.2% 59.8%;
  }
}

@layer base {
  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground;
  }
}
import ByteBuddy from "@/components/ByteBuddy";

const Index = () => {
  return <ByteBuddy />;
};

export default Index;
import type { Config } from "tailwindcss";

export default {
	darkMode: ["class"],
	content: [
		"./pages/**/*.{ts,tsx}",
		"./components/**/*.{ts,tsx}",
		"./app/**/*.{ts,tsx}",
		"./src/**/*.{ts,tsx}",
	],
	prefix: "",
	theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
		extend: {
			colors: {
				border: 'hsl(var(--border))',
				input: 'hsl(var(--input))',
				ring: 'hsl(var(--ring))',
				background: 'hsl(var(--background))',
				foreground: 'hsl(var(--foreground))',
				primary: {
					DEFAULT: 'hsl(var(--primary))',
					foreground: 'hsl(var(--primary-foreground))'
				},
				secondary: {
					DEFAULT: 'hsl(var(--secondary))',
					foreground: 'hsl(var(--secondary-foreground))'
				},
				destructive: {
					DEFAULT: 'hsl(var(--destructive))',
					foreground: 'hsl(var(--destructive-foreground))'
				},
				muted: {
					DEFAULT: 'hsl(var(--muted))',
					foreground: 'hsl(var(--muted-foreground))'
				},
				accent: {
					DEFAULT: 'hsl(var(--accent))',
					foreground: 'hsl(var(--accent-foreground))'
				},
				popover: {
					DEFAULT: 'hsl(var(--popover))',
					foreground: 'hsl(var(--popover-foreground))'
				},
				card: {
					DEFAULT: 'hsl(var(--card))',
					foreground: 'hsl(var(--card-foreground))'
				},
				sidebar: {
					DEFAULT: 'hsl(var(--sidebar-background))',
					foreground: 'hsl(var(--sidebar-foreground))',
					primary: 'hsl(var(--sidebar-primary))',
					'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
					accent: 'hsl(var(--sidebar-accent))',
					'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
					border: 'hsl(var(--sidebar-border))',
					ring: 'hsl(var(--sidebar-ring))'
				},
				// ByteBuddy Design System
				'electric-blue': 'hsl(var(--electric-blue))',
				'warm-orange': 'hsl(var(--warm-orange))',
				'magic-purple': 'hsl(var(--magic-purple))',
				'tech-cyan': 'hsl(var(--tech-cyan))',
				'soft-gray': 'hsl(var(--soft-gray))'
			},
			backgroundImage: {
				'gradient-electric': 'var(--gradient-electric)',
				'gradient-warm': 'var(--gradient-warm)',
				'gradient-tech': 'var(--gradient-tech)'
			},
			boxShadow: {
				'electric': 'var(--shadow-electric)',
				'warm': 'var(--shadow-warm)',
				'glow': 'var(--shadow-glow)'
			},
			transitionTimingFunction: {
				'smooth': 'var(--transition-smooth)',
				'bounce-in': 'var(--transition-bounce)'
			},
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			keyframes: {
				'accordion-down': {
					from: {
						height: '0'
					},
					to: {
						height: 'var(--radix-accordion-content-height)'
					}
				},
				'accordion-up': {
					from: {
						height: 'var(--radix-accordion-content-height)'
					},
					to: {
						height: '0'
					}
				},
				// ByteBuddy Animations
				'bounce-in': {
					'0%': {
						transform: 'scale(0.3)',
						opacity: '0'
					},
					'50%': {
						transform: 'scale(1.05)'
					},
					'70%': {
						transform: 'scale(0.9)'
					},
					'100%': {
						transform: 'scale(1)',
						opacity: '1'
					}
				},
				'fade-scale': {
					'0%': {
						opacity: '0',
						transform: 'scale(0.95)'
					},
					'100%': {
						opacity: '1',
						transform: 'scale(1)'
					}
				},
				'robot-pulse': {
					'0%, 100%': {
						transform: 'scale(1)',
						opacity: '1'
					},
					'50%': {
						transform: 'scale(1.02)',
						opacity: '0.8'
					}
				},
				'glow-pulse': {
					'0%, 100%': {
						boxShadow: '0 0 20px hsl(195 100% 50% / 0.2)'
					},
					'50%': {
						boxShadow: '0 0 40px hsl(195 100% 50% / 0.4)'
					}
				}
			},
			animation: {
				'accordion-down': 'accordion-down 0.2s ease-out',
				'accordion-up': 'accordion-up 0.2s ease-out',
				// ByteBuddy Animations
				'bounce-in': 'bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
				'fade-scale': 'fade-scale 0.3s ease-out',
				'robot-pulse': 'robot-pulse 2s ease-in-out infinite',
				'glow-pulse': 'glow-pulse 3s ease-in-out infinite'
			}
		}
	},
	plugins: [require("tailwindcss-animate")],
} satisfies Config;