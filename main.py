"""
World Football Championship
193-country knockout tournament
Kivy + Buildozer compatible

Project structure:
    main.py
    flags/
        af.png
        al.png
        ...
        pk.png
        ...
        zw.png

Flags must use lowercase ISO alpha-2 filenames.
"""

import math
import os
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import (
    Color, Ellipse, Line, Rectangle,
    StencilPop, StencilPush, StencilUnUse, StencilUse,
)
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

FLAGS_DIR = "flags"
BALL_RADIUS = 60

# 193 UN member states / ISO alpha-2 codes used by the uploaded draft.
COUNTRIES = [
    ('Afghanistan', 'af'),
    ('Albania', 'al'),
    ('Algeria', 'dz'),
    ('Andorra', 'ad'),
    ('Angola', 'ao'),
    ('Antigua and Barbuda', 'ag'),
    ('Argentina', 'ar'),
    ('Armenia', 'am'),
    ('Australia', 'au'),
    ('Austria', 'at'),
    ('Azerbaijan', 'az'),
    ('Bahamas', 'bs'),
    ('Bahrain', 'bh'),
    ('Bangladesh', 'bd'),
    ('Barbados', 'bb'),
    ('Belarus', 'by'),
    ('Belgium', 'be'),
    ('Belize', 'bz'),
    ('Benin', 'bj'),
    ('Bhutan', 'bt'),
    ('Bolivia', 'bo'),
    ('Bosnia and Herzegovina', 'ba'),
    ('Botswana', 'bw'),
    ('Brazil', 'br'),
    ('Brunei', 'bn'),
    ('Bulgaria', 'bg'),
    ('Burkina Faso', 'bf'),
    ('Burundi', 'bi'),
    ('Cabo Verde', 'cv'),
    ('Cambodia', 'kh'),
    ('Cameroon', 'cm'),
    ('Canada', 'ca'),
    ('Central African Republic', 'cf'),
    ('Chad', 'td'),
    ('Chile', 'cl'),
    ('China', 'cn'),
    ('Colombia', 'co'),
    ('Comoros', 'km'),
    ('Congo', 'cg'),
    ('Costa Rica', 'cr'),
    ("Cote d'Ivoire", 'ci'),
    ('Croatia', 'hr'),
    ('Cuba', 'cu'),
    ('Cyprus', 'cy'),
    ('Czechia', 'cz'),
    ('DPR Korea', 'kp'),
    ('DRC', 'cd'),
    ('Denmark', 'dk'),
    ('Djibouti', 'dj'),
    ('Dominica', 'dm'),
    ('Dominican Republic', 'do'),
    ('Ecuador', 'ec'),
    ('Egypt', 'eg'),
    ('El Salvador', 'sv'),
    ('Equatorial Guinea', 'gq'),
    ('Eritrea', 'er'),
    ('Estonia', 'ee'),
    ('Eswatini', 'sz'),
    ('Ethiopia', 'et'),
    ('Fiji', 'fj'),
    ('Finland', 'fi'),
    ('France', 'fr'),
    ('Gabon', 'ga'),
    ('Gambia', 'gm'),
    ('Georgia', 'ge'),
    ('Germany', 'de'),
    ('Ghana', 'gh'),
    ('Greece', 'gr'),
    ('Grenada', 'gd'),
    ('Guatemala', 'gt'),
    ('Guinea', 'gn'),
    ('Guinea-Bissau', 'gw'),
    ('Guyana', 'gy'),
    ('Haiti', 'ht'),
    ('Honduras', 'hn'),
    ('Hungary', 'hu'),
    ('Iceland', 'is'),
    ('India', 'in'),
    ('Indonesia', 'id'),
    ('Iran', 'ir'),
    ('Iraq', 'iq'),
    ('Ireland', 'ie'),
    ('Palestine', 'ps'),
    ('Italy', 'it'),
    ('Jamaica', 'jm'),
    ('Japan', 'jp'),
    ('Jordan', 'jo'),
    ('Kazakhstan', 'kz'),
    ('Kenya', 'ke'),
    ('Kiribati', 'ki'),
    ('Kuwait', 'kw'),
    ('Kyrgyzstan', 'kg'),
    ('Laos', 'la'),
    ('Latvia', 'lv'),
    ('Lebanon', 'lb'),
    ('Lesotho', 'ls'),
    ('Liberia', 'lr'),
    ('Libya', 'ly'),
    ('Liechtenstein', 'li'),
    ('Lithuania', 'lt'),
    ('Luxembourg', 'lu'),
    ('Madagascar', 'mg'),
    ('Malawi', 'mw'),
    ('Malaysia', 'my'),
    ('Maldives', 'mv'),
    ('Mali', 'ml'),
    ('Malta', 'mt'),
    ('Marshall Islands', 'mh'),
    ('Mauritania', 'mr'),
    ('Mauritius', 'mu'),
    ('Mexico', 'mx'),
    ('Micronesia', 'fm'),
    ('Monaco', 'mc'),
    ('Mongolia', 'mn'),
    ('Montenegro', 'me'),
    ('Morocco', 'ma'),
    ('Mozambique', 'mz'),
    ('Myanmar', 'mm'),
    ('Namibia', 'na'),
    ('Nauru', 'nr'),
    ('Nepal', 'np'),
    ('Netherlands', 'nl'),
    ('New Zealand', 'nz'),
    ('Nicaragua', 'ni'),
    ('Niger', 'ne'),
    ('Nigeria', 'ng'),
    ('North Macedonia', 'mk'),
    ('Norway', 'no'),
    ('Oman', 'om'),
    ('Pakistan', 'pk'),
    ('Palau', 'pw'),
    ('Panama', 'pa'),
    ('Papua New Guinea', 'pg'),
    ('Paraguay', 'py'),
    ('Peru', 'pe'),
    ('Philippines', 'ph'),
    ('Poland', 'pl'),
    ('Portugal', 'pt'),
    ('Qatar', 'qa'),
    ('South Korea', 'kr'),
    ('Moldova', 'md'),
    ('Romania', 'ro'),
    ('Russia', 'ru'),
    ('Rwanda', 'rw'),
    ('Saint Kitts and Nevis', 'kn'),
    ('Saint Lucia', 'lc'),
    ('Saint Vincent', 'vc'),
    ('Samoa', 'ws'),
    ('San Marino', 'sm'),
    ('Sao Tome', 'st'),
    ('Saudi Arabia', 'sa'),
    ('Senegal', 'sn'),
    ('Serbia', 'rs'),
    ('Seychelles', 'sc'),
    ('Sierra Leone', 'sl'),
    ('Singapore', 'sg'),
    ('Slovakia', 'sk'),
    ('Slovenia', 'si'),
    ('Solomon Islands', 'sb'),
    ('Somalia', 'so'),
    ('South Africa', 'za'),
    ('South Sudan', 'ss'),
    ('Spain', 'es'),
    ('Sri Lanka', 'lk'),
    ('Sudan', 'sd'),
    ('Suriname', 'sr'),
    ('Sweden', 'se'),
    ('Switzerland', 'ch'),
    ('Syria', 'sy'),
    ('Tajikistan', 'tj'),
    ('Tanzania', 'tz'),
    ('Thailand', 'th'),
    ('Timor-Leste', 'tl'),
    ('Togo', 'tg'),
    ('Tonga', 'to'),
    ('Trinidad and Tobago', 'tt'),
    ('Tunisia', 'tn'),
    ('Turkey', 'tr'),
    ('Turkmenistan', 'tm'),
    ('Tuvalu', 'tv'),
    ('Uganda', 'ug'),
    ('Ukraine', 'ua'),
    ('UAE', 'ae'),
    ('UK', 'gb'),
    ('USA', 'us'),
    ('Uruguay', 'uy'),
    ('Uzbekistan', 'uz'),
    ('Vanuatu', 'vu'),
    ('Venezuela', 've'),
    ('Vietnam', 'vn'),
    ('Yemen', 'ye'),
    ('Zambia', 'zm'),
    ('Zimbabwe', 'zw'),
]

assert len(COUNTRIES) == 193, f"Expected 193 countries, got {len(COUNTRIES)}"


def get_flag_path(code):
    """Find a flag in common Kivy/Buildozer locations."""
    filename = f"{code.lower()}.png"
    candidates = (
        os.path.join(FLAGS_DIR, filename),
        os.path.join(os.path.dirname(__file__), FLAGS_DIR, filename),
        os.path.join(os.getcwd(), FLAGS_DIR, filename),
    )
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


# ---------------------------------------------------------------------------
# TOURNAMENT
# ---------------------------------------------------------------------------

class Tournament:
    def __init__(self):
        self.all_countries = COUNTRIES[:]
        self.reset()

    def reset(self):
        self.round_teams = self.all_countries[:]
        random.shuffle(self.round_teams)

        self.round_num = 1
        self.match_index = 0
        self.matches = []
        self.winners = []
        self.champion = None
        self.bye_team = None

        self._prepare_round()

    def _prepare_round(self):
        teams = self.round_teams[:]
        random.shuffle(teams)

        self.matches = []
        self.winners = []
        self.bye_team = None
        self.match_index = 0

        if len(teams) % 2:
            self.bye_team = teams.pop()
            self.winners.append(self.bye_team)

        for i in range(0, len(teams), 2):
            self.matches.append((teams[i], teams[i + 1]))

    def get_current_match(self):
        if self.match_index < len(self.matches):
            return self.matches[self.match_index]
        return None

    def record_match_winner(self, winner):
        self.winners.append(winner)
        self.match_index += 1

        if self.match_index >= len(self.matches):
            self.round_teams = self.winners[:]
            self.round_num += 1

            if len(self.round_teams) == 1:
                self.champion = self.round_teams[0]
                return True

            self._prepare_round()

        return False

    def get_progress_text(self):
        total = max(1, len(self.matches))
        return f"Round {self.round_num}  •  Match {self.match_index + 1}/{total}"


# ---------------------------------------------------------------------------
# FOOTBALL
# ---------------------------------------------------------------------------

class Football(Widget):
    vx = NumericProperty(0)
    vy = NumericProperty(0)
    spin = NumericProperty(0)
    angle = NumericProperty(0)

    def __init__(self, country_data, **kwargs):
        super().__init__(**kwargs)

        self.country_data = country_data
        self.country_name, self.country_code = country_data
        self.radius = BALL_RADIUS
        self.size = (self.radius * 2, self.radius * 2)

        self.mass = 1.0
        self.flag_texture = None

        flag_path = get_flag_path(self.country_code)
        if flag_path:
            try:
                self.flag_texture = CoreImage(flag_path).texture
            except Exception:
                self.flag_texture = None

        self._draw()

    def _draw(self):
        self.canvas.clear()

        with self.canvas:
            Color(0, 0, 0, 0.28)
            Ellipse(
                pos=(self.x + 4, self.y - 5),
                size=self.size,
            )

            StencilPush()
            Ellipse(pos=self.pos, size=self.size)
            StencilUse()

            if self.flag_texture is not None:
                Color(1, 1, 1, 1)
                Rectangle(
                    pos=self.pos,
                    size=self.size,
                    texture=self.flag_texture,
                )
            else:
                Color(0.25, 0.35, 0.45, 1)
                Ellipse(pos=self.pos, size=self.size)

            StencilUnUse()
            StencilPop()

            Color(1, 1, 1, 0.22)
            Ellipse(
                pos=(self.x + 7, self.y + 14),
                size=(self.radius * 0.75, self.radius * 0.55),
            )

            Color(0, 0, 0, 0.22)
            Ellipse(
                pos=(self.x + 18, self.y + 1),
                size=(self.radius * 0.8, self.radius * 0.65),
            )

            Color(1, 1, 1, 0.7)
            Line(
                circle=(self.center_x, self.center_y, self.radius),
                width=1.5,
            )

    def set_center(self, cx, cy):
        self.pos = (
            cx - self.radius,
            cy - self.radius,
        )
        self._draw()

    def on_pos(self, *_):
        self._draw()


# ---------------------------------------------------------------------------
# ARENA
# ---------------------------------------------------------------------------

class Arena(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ball1 = None
        self.ball2 = None
        self.match_callback = None

        self.state = "IDLE"
        self.goal_scored = False
        self.winner = None

        # Goal Dimensions
        self.goal_height = 200     # Opening height
        self.goal_depth = 50       # Depth extending outside field walls
        self.goal_y_start = 0

        # Ball Physics & Speed Controls
        self.speed_multiplier = 1.002  # Gradual acceleration (1.0 = static speed)
        self.max_ball_speed = 600.0   # Fixed upper cap for speed (pixels/sec)

        self.gravity = 0.0
        self.central_force = 20.0
        self.wall_restitution = 1.20
        self.floor_restitution = 1.20
        self.ball_restitution = 1.20
        self.friction = 1.0
        self.min_bounce = 200.0
        self.match_time = 0.0
        self.max_match_time = 30.0

        self.countdown_label = None
        self.winner_overlay = None
        self.winner_flag = None

        Clock.schedule_interval(self.update, 1 / 60)

    def setup_match(self, team1, team2):
        self.state = "COUNTDOWN"
        self.goal_scored = False
        self.winner = None
        self.match_time = 0.0

        self._remove_widget_safe(self.ball1)
        self._remove_widget_safe(self.ball2)
        self._remove_widget_safe(self.countdown_label)
        self._remove_widget_safe(self.winner_overlay)
        self._remove_widget_safe(self.winner_flag)

        self.ball1 = Football(team1)
        self.ball2 = Football(team2)

        cx = self.x + self.width / 2
        cy = self.y + self.height / 2

        self.ball1.set_center(cx - 80, cy + 20)
        self.ball2.set_center(cx + 80, cy - 20)

        self.ball1.vx = random.uniform(250, 400)
        self.ball1.vy = random.uniform(-200, 200)

        self.ball2.vx = random.uniform(-400, -250)
        self.ball2.vy = random.uniform(-200, 200)

        self.ball1.spin = random.uniform(-5, 5)
        self.ball2.spin = random.uniform(-5, 5)

        self.add_widget(self.ball1)
        self.add_widget(self.ball2)

        self.countdown_value = 3
        self._show_countdown()

    def _remove_widget_safe(self, widget):
        if widget is not None and widget.parent is self:
            self.remove_widget(widget)

    def _show_countdown(self):
        self._remove_widget_safe(self.countdown_label)
        self.countdown_label = None

        if self.countdown_value > 0:
            self.countdown_label = Label(
                text=str(self.countdown_value),
                font_size=max(48, min(self.width, self.height) * 0.24),
                bold=True,
                color=(1, 0.85, 0.1, 1),
                outline_color=(0, 0, 0, 1),
                outline_width=4,
                halign="center",
                valign="middle",
            )
            self.countdown_label.size = self.size
            self.countdown_label.pos = self.pos
            self.add_widget(self.countdown_label)

            self.countdown_value -= 1
            Clock.schedule_once(lambda dt: self._show_countdown(), 1.0)
        else:
            self.countdown_label = Label(
                text="GO!",
                font_size=max(42, min(self.width, self.height) * 0.20),
                bold=True,
                color=(0.2, 1, 0.3, 1),
                outline_color=(0, 0, 0, 1),
                outline_width=4,
                halign="center",
                valign="middle",
            )
            self.countdown_label.size = self.size
            self.countdown_label.pos = self.pos
            self.add_widget(self.countdown_label)
            Clock.schedule_once(self._start_play, 0.45)

    def _start_play(self, _dt):
        self._remove_widget_safe(self.countdown_label)
        self.countdown_label = None
        if not self.goal_scored:
            self.state = "PLAYING"

    def update(self, dt):
        if self.state != "PLAYING" or self.goal_scored:
            return

        dt = min(dt, 0.035)
        self.match_time += dt

        if self.match_time >= self.max_match_time:
            winner = random.choice([self.ball1.country_data, self.ball2.country_data])
            self._on_goal_scored(
                "left" if winner == self.ball1.country_data else "right"
            )
            return

        goal_y_bottom = self.y + self.goal_y_start
        goal_y_top = goal_y_bottom + self.goal_height

        for ball in (self.ball1, self.ball2):
            ball.vy += self.gravity * dt

            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            bx = ball.x + ball.radius
            by = ball.y + ball.radius

            dx = cx - bx
            dy = cy - by
            distance = max(1.0, math.hypot(dx, dy))

            ball.vx += self.central_force * dx / distance * dt
            ball.vy += self.central_force * dy / distance * dt

            ball.vx += random.uniform(-7, 7) * dt
            ball.vy += random.uniform(-7, 7) * dt

            ball.vx *= self.friction
            ball.vy *= self.friction

            # Apply Speed Multiplier & Ceiling Cap
            ball.vx *= self.speed_multiplier
            ball.vy *= self.speed_multiplier

            current_speed = math.hypot(ball.vx, ball.vy)
            if current_speed > self.max_ball_speed:
                scale = self.max_ball_speed / current_speed
                ball.vx *= scale
                ball.vy *= scale

            ball.x += ball.vx * dt
            ball.y += ball.vy * dt

            ball.angle += ball.spin * dt * 60
            ball.spin *= 0.992

            # Left goal / wall (Bounded to Arena self.x)
            if ball.x <= self.x - ball.radius:
                if goal_y_bottom <= ball.y + ball.radius <= goal_y_top:
                    self._on_goal_scored("left")
                    return
                ball.x = self.x
                ball.vx = abs(ball.vx) * self.wall_restitution

            # Right goal / wall (Bounded to Arena self.x + self.width)
            if ball.x + ball.radius >= self.x + self.width + ball.radius:
                if goal_y_bottom <= ball.y + ball.radius <= goal_y_top:
                    self._on_goal_scored("right")
                    return
                ball.x = self.x + self.width - 2 * ball.radius
                ball.vx = -abs(ball.vx) * self.wall_restitution

            # Floor (Bounded to Arena self.y)
            if ball.y < self.y:
                ball.y = self.y
                ball.vy = abs(ball.vy) * self.floor_restitution
                if abs(ball.vy) < self.min_bounce:
                    ball.vy = self.min_bounce

            # Ceiling (Bounded to Arena self.y + self.height)
            if ball.y + 2 * ball.radius > self.y + self.height:
                ball.y = self.y + self.height - 2 * ball.radius
                ball.vy = -abs(ball.vy) * self.wall_restitution

        self._resolve_ball_collision()

        self.ball1._draw()
        self.ball2._draw()

    def _resolve_ball_collision(self):
        b1, b2 = self.ball1, self.ball2

        x1 = b1.x + b1.radius
        y1 = b1.y + b1.radius
        x2 = b2.x + b2.radius
        y2 = b2.y + b2.radius

        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)

        min_distance = b1.radius + b2.radius
        if distance <= 0 or distance >= min_distance:
            return

        nx = dx / distance
        ny = dy / distance

        overlap = min_distance - distance
        b1.x -= nx * overlap * 0.5
        b1.y -= ny * overlap * 0.5
        b2.x += nx * overlap * 0.5
        b2.y += ny * overlap * 0.5

        relative_vx = b2.vx - b1.vx
        relative_vy = b2.vy - b1.vy
        velocity_normal = relative_vx * nx + relative_vy * ny

        if velocity_normal > 0:
            return

        impulse = -(1 + self.ball_restitution) * velocity_normal
        impulse /= (1 / b1.mass + 1 / b2.mass)

        ix = impulse * nx
        iy = impulse * ny

        b1.vx -= ix / b1.mass
        b1.vy -= iy / b1.mass
        b2.vx += ix / b2.mass
        b2.vy += iy / b2.mass

        b1.spin += random.uniform(-3, 3)
        b2.spin += random.uniform(-3, 3)

        for ball in (b1, b2):
            speed = math.hypot(ball.vx, ball.vy)
            if speed < 90:
                scale = 90 / max(speed, 1)
                ball.vx *= scale
                ball.vy *= scale
            elif speed > self.max_ball_speed:
                scale = self.max_ball_speed / speed
                ball.vx *= scale
                ball.vy *= scale

    def _on_goal_scored(self, side):
        if self.goal_scored:
            return

        self.goal_scored = True
        self.state = "GOAL"

        if side == "left":
            self.winner = self.ball2.country_data
        else:
            self.winner = self.ball1.country_data

        self._show_winner()

    def _show_winner(self):
        self._remove_widget_safe(self.winner_overlay)
        self._remove_widget_safe(self.winner_flag)

        name, code = self.winner

        self.winner_overlay = Label(
            text=f"{name} WINS!",
            font_size=max(28, min(self.width, self.height) * 0.10),
            bold=True,
            color=(1, 0.84, 0.1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=4,
            halign="center",
            valign="middle",
        )
        self.winner_overlay.size = (self.width, self.height * 0.28)
        self.winner_overlay.pos = (self.x, self.y + self.height * 0.36)
        self.add_widget(self.winner_overlay)

        flag_path = get_flag_path(code)
        if flag_path:
            self.winner_flag = Image(
                source=flag_path,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(None, None),
            )
            fw = min(self.width * 0.38, 180)
            self.winner_flag.size = (fw, fw * 0.67)
            self.winner_flag.pos = (
                self.x + (self.width - self.winner_flag.width) / 2,
                self.y + self.height * 0.60,
            )
            self.add_widget(self.winner_flag)

        Clock.schedule_once(self._end_match, 2.0)

    def _end_match(self, _dt):
        self._remove_widget_safe(self.winner_overlay)
        self._remove_widget_safe(self.winner_flag)

        self.winner_overlay = None
        self.winner_flag = None

        if self.match_callback:
            self.match_callback(self.winner)

    def on_size(self, *_):
        self.goal_y_start = max(0, (self.height - self.goal_height) / 2)
        self._draw_arena()

    def on_pos(self, *_):
        self.goal_y_start = max(0, (self.height - self.goal_height) / 2)
        self._draw_arena()

    def _draw_arena(self):
        self.canvas.before.clear()

        with self.canvas.before:
            Color(0.08, 0.42, 0.10, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(1, 1, 1, 0.65)

            # Halfway line.
            Line(
                points=[
                    self.x + self.width / 2, self.y,
                    self.x + self.width / 2, self.y + self.height,
                ],
                width=2,
            )

            # Center circle.
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            Line(
                circle=(cx, cy, min(self.width, self.height) * 0.15),
                width=2,
            )
            Ellipse(
                pos=(cx - 3, cy - 3),
                size=(6, 6),
            )

            goal_y = self.y + self.goal_y_start

            # Left goal.
            Line(
                rectangle=(self.x - 3, goal_y, 6, self.goal_height),
                width=3,
            )
            for i in range(6):
                y = goal_y + self.goal_height * i / 5
                Line(
                    points=[self.x - self.goal_depth, y, self.x, y],
                    width=1,
                )

            # Right goal.
            Line(
                rectangle=(
                    self.x + self.width - 3,
                    goal_y,
                    6,
                    self.goal_height,
                ),
                width=3,
            )
            for i in range(6):
                y = goal_y + self.goal_height * i / 5
                Line(
                    points=[
                        self.x + self.width,
                        y,
                        self.x + self.width + self.goal_depth,
                        y,
                    ],
                    width=1,
                )

            # Outer boundary, with goal openings.
            Color(1, 1, 1, 0.85)
            Line(
                points=[self.x, self.y, self.x + self.width, self.y],
                width=2,
            )
            Line(
                points=[
                    self.x,
                    self.y + self.height,
                    self.x + self.width,
                    self.y + self.height,
                ],
                width=2,
            )
            Line(
                points=[
                    self.x,
                    self.y,
                    self.x,
                    goal_y,
                ],
                width=2,
            )
            Line(
                points=[
                    self.x,
                    goal_y + self.goal_height,
                    self.x,
                    self.y + self.height,
                ],
                width=2,
            )
            Line(
                points=[
                    self.x + self.width,
                    self.y,
                    self.x + self.width,
                    goal_y,
                ],
                width=2,
            )
            Line(
                points=[
                    self.x + self.width,
                    goal_y + self.goal_height,
                    self.x + self.width,
                    self.y + self.height,
                ],
                width=2,
            )


# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------

class MatchHeader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.padding = 10
        self.spacing = 8

        with self.canvas.before:
            Color(0.025, 0.035, 0.06, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

        self.left_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.4, 1),
            spacing=3,
        )
        self.left_flag = Image(
            size_hint=(1, 0.65),
            allow_stretch=True,
            keep_ratio=True,
        )
        self.left_name = Label(
            font_size="16sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.35),
        )
        self.left_box.add_widget(self.left_flag)
        self.left_box.add_widget(self.left_name)

        self.center_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.2, 1),
        )
        self.vs_label = Label(
            text="VS",
            font_size="25sp",
            bold=True,
            color=(1, 0.82, 0.05, 1),
        )
        self.info_label = Label(
            text="",
            font_size="11sp",
            halign="center",
            valign="middle",
        )
        self.center_box.add_widget(self.vs_label)
        self.center_box.add_widget(self.info_label)

        self.right_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.4, 1),
            spacing=3,
        )
        self.right_flag = Image(
            size_hint=(1, 0.65),
            allow_stretch=True,
            keep_ratio=True,
        )
        self.right_name = Label(
            font_size="16sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.35),
        )
        self.right_box.add_widget(self.right_flag)
        self.right_box.add_widget(self.right_name)

        self.add_widget(self.left_box)
        self.add_widget(self.center_box)
        self.add_widget(self.right_box)

        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def set_match(self, team1, team2, info_text):
        name1, code1 = team1
        name2, code2 = team2

        self.left_name.text = name1
        self.right_name.text = name2
        self.info_label.text = info_text

        self.left_flag.source = get_flag_path(code1) or ""
        self.right_flag.source = get_flag_path(code2) or ""

        self.left_flag.reload()
        self.right_flag.reload()


# ---------------------------------------------------------------------------
# CHAMPION SCREEN
# ---------------------------------------------------------------------------

class ChampionScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = None
        self.flag = None
        self.opacity = 0

    def show_champion(self, country_data):
        self.hide()

        name, code = country_data

        with self.canvas:
            Color(0.01, 0.01, 0.02, 0.94)
            self.overlay = Rectangle(pos=self.pos, size=self.size)

        flag_path = get_flag_path(code)
        if flag_path:
            self.flag = Image(
                source=flag_path,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(None, None),
            )
            fw = min(self.width * 0.58, 280)
            self.flag.size = (fw, fw * 0.67)
            self.flag.pos = (
                self.x + (self.width - fw) / 2,
                self.y + self.height * 0.47,
            )
            self.add_widget(self.flag)

        self.label = Label(
            text=f"🏆 CHAMPION 🏆\n{name}",
            font_size=max(30, min(self.width, self.height) * 0.075),
            bold=True,
            color=(1, 0.84, 0.1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=4,
            halign="center",
            valign="middle",
        )
        self.label.size = (self.width, self.height * 0.25)
        self.label.pos = (self.x, self.y + self.height * 0.18)
        self.add_widget(self.label)

        self.opacity = 1

    def hide(self):
        if self.label is not None and self.label.parent is self:
            self.remove_widget(self.label)
        if self.flag is not None and self.flag.parent is self:
            self.remove_widget(self.flag)

        self.label = None
        self.flag = None
        self.canvas.clear()
        self.opacity = 0


# ---------------------------------------------------------------------------
# MAIN GAME
# ---------------------------------------------------------------------------

class WorldFootballGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tournament = Tournament()

        self.header = MatchHeader()
        self.arena = Arena()
        self.arena.match_callback = self.on_match_end

        self.champion_screen = ChampionScreen()

        self.add_widget(self.header)
        self.add_widget(self.arena)
        self.add_widget(self.champion_screen)

        self.bind(pos=self._update_layout, size=self._update_layout)
        Clock.schedule_once(lambda dt: self.start_next_match(), 0.2)

    def _update_layout(self, *_):
        w, h = self.size

        header_h = w * 5 / 9
        arena_h = w

        if header_h + arena_h > h:
            scale = h / max(1, header_h + arena_h)
            header_h *= scale
            arena_h *= scale

        self.header.pos = (self.x, self.y + h - header_h)
        self.header.size = (w, header_h)

        self.arena.pos = (
            self.x,
            self.y + h - header_h - arena_h,
        )
        self.arena.size = (w, arena_h)

        self.champion_screen.pos = self.pos
        self.champion_screen.size = self.size

    def start_next_match(self):
        match = self.tournament.get_current_match()

        if match is None:
            self.show_champion()
            return

        team1, team2 = match

        self.header.set_match(
            team1,
            team2,
            self.tournament.get_progress_text(),
        )
        self.arena.setup_match(team1, team2)

    def on_match_end(self, winner):
        tournament_over = self.tournament.record_match_winner(winner)

        if tournament_over:
            self.show_champion()
        else:
            Clock.schedule_once(
                lambda dt: self.start_next_match(),
                0.45,
            )

    def show_champion(self):
        champion = self.tournament.champion
        if champion is None:
            return

        self.champion_screen.show_champion(champion)
        Clock.schedule_once(lambda dt: self.restart_tournament(), 4.0)

    def restart_tournament(self):
        self.champion_screen.hide()
        self.tournament.reset()
        self.start_next_match()


class WorldFootballApp(App):
    def build(self):
        Window.clearcolor = (0.01, 0.01, 0.02, 1)
        return WorldFootballGame()


if __name__ == "__main__":
    WorldFootballApp().run()
