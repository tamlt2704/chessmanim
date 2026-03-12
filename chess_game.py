from manim import *
import manim_chess
import chess
import chess.pgn
import re

# Configuration
MAX_MOVES = -1  # Change this to render more or fewer moves

class ChessGame(Scene):
    def construct(self):
        with open('steinitz_bardeleben.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        
        board = game.board()
        
        # Game header information - display line by line
        event = game.headers.get("Event", "")
        site = game.headers.get("Site", "")
        date = game.headers.get("Date", "")
        round_num = game.headers.get("Round", "")
        white = game.headers.get("White", "")
        black = game.headers.get("Black", "")
        result = game.headers.get("Result", "")
        eco = game.headers.get("ECO", "")
        ply_count_header = game.headers.get("PlyCount", "")
        event_date = game.headers.get("EventDate", "")
        
        header_lines = [
            f"Event: {event}",
            f"Site: {site}",
            f"Date: {date}",
            f"Round: {round_num}",
            f"White: {white}",
            f"Black: {black}",
            f"Result: {result}",
            f"ECO: {eco}",
            f"PlyCount: {ply_count_header}",
            f"EventDate: {event_date}"
        ]
        
        # Create chess board
        chess_board = manim_chess.Board()
        chess_board.set_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        chess_board.set_width(config.frame_width * 0.45)
        chess_board.shift(LEFT * 2.5 + UP * 0.3)
        self.play(FadeIn(chess_board))
        self.wait()
        
        # Convert moves to manim_chess format
        moves = []
        for node in game.mainline():
            move = node.move
            from_square = chess.square_name(move.from_square)
            to_square = chess.square_name(move.to_square)
            promotion = chess.piece_name(move.promotion) if move.promotion else ''
            moves.append((from_square, to_square, promotion))
        
        total_plies = len(moves)
        total_moves = (total_plies + 1) // 2
        
        # Progress bar (aligned with board)
        board_width = chess_board.get_width()
        
        progress_bg = Rectangle(width=board_width, height=0.3, fill_color=GRAY, fill_opacity=0.5, stroke_width=2)
        progress_bg.align_to(chess_board, LEFT).shift(DOWN * 3.5)
        progress_bar = Rectangle(width=0, height=0.3, fill_color=BLUE, fill_opacity=0.8, stroke_width=0)
        progress_bar.move_to(progress_bg.get_center())
        progress_bar.align_to(progress_bg, LEFT)
        progress_text = Text(f"Move 0/{total_moves}", font_size=18).next_to(progress_bg, RIGHT, buff=0.3)
        
        self.add(progress_bg, progress_bar, progress_text)
        
        # Now display game info aligned with progress text and board
        game_info_text = ""
        game_info_pos = progress_bg.get_right() + RIGHT * 0.5 + UP * (chess_board.get_top()[1] - progress_bg.get_right()[1])
        game_info = Text("Loading...", font_size=18, line_spacing=0.9).move_to(game_info_pos, aligned_edge=LEFT+UP)
        self.add(game_info)
        
        for line in header_lines:
            game_info_text += line + "\n"
            new_game_info = Text(game_info_text.strip(), font_size=18, line_spacing=0.9).move_to(game_info_pos, aligned_edge=LEFT+UP)
            self.play(Transform(game_info, new_game_info), run_time=0.3)
        
        self.wait()
        
        # Move counter and annotation area (below game info)
        annotation_text_pos = game_info_pos + DOWN * 4
        annotation_text = Text(" ", font_size=16, color=GOLD).move_to(annotation_text_pos, aligned_edge=LEFT+UP)
        annotation_text.set_max_width(5)
        
        self.add(annotation_text)
        
        # Move display next to progress bar at bottom
        move_text_pos = progress_text.get_right() + RIGHT * 0.5
        move_text = Text("Loading", font_size=18).move_to(move_text_pos, aligned_edge=LEFT)
        move_text.align_to(progress_text, DOWN)
        move_text.set_max_width(5)
        
        self.add(move_text)
        
        # Track current move pair
        white_move = ""
        
        # Play through the game
        ply_count = 0
        for i, node in enumerate(game.mainline()):
            ply_count += 1
            if MAX_MOVES > 0 and ply_count > MAX_MOVES * 2:
                break
                
            move = node.move
            san_move = board.san(move)
            
            move_num = (ply_count + 1) // 2
            is_white = (ply_count % 2 == 1)
            
            comment = node.comment if node.comment else ""
            has_diagram = '[pgndiagram]' in comment
            print(f"Ply {ply_count} Move {move_num}: {san_move} - has_diagram: {has_diagram}, comment: {comment if comment else 'None'}")
            comment = re.sub(r'\[pgndiagram\]', '', comment).strip()
            comment = ' '.join(comment.split())
            
            # Build current move text showing both white and black moves
            if is_white:
                white_move = san_move
                current_move_text = f"{move_num}. {san_move}"
            else:
                current_move_text = f"{move_num}. {white_move}, {san_move}"
            
            new_move_text = Text(current_move_text, font_size=18, color=WHITE).move_to(move_text_pos, aligned_edge=LEFT)
            new_move_text.align_to(progress_text, DOWN)
            new_move_text.set_max_width(5)
            
            # Display full comment if exists
            if comment:
                new_annotation = Text(comment, font_size=16, color=GOLD).move_to(annotation_text_pos, aligned_edge=LEFT+UP)
                new_annotation.set_max_width(5)
                self.play(
                    Transform(move_text, new_move_text),
                    run_time=0.3
                )
                self.play(Write(new_annotation), run_time=0.5)
                self.remove(annotation_text)
                annotation_text = new_annotation
                self.add(annotation_text)
            else:
                self.play(
                    Transform(move_text, new_move_text),
                    FadeOut(annotation_text),
                    run_time=0.3
                )
                annotation_text = Text(" ", font_size=16, color=GOLD).move_to(annotation_text_pos, aligned_edge=LEFT+UP)
                self.add(annotation_text)
            
            self.wait(0.5)
            
            # Animate the move AFTER displaying text
            manim_chess.play_game(scene=self, board=chess_board, moves=[moves[i]])
            board.push(move)
            
            # Update progress bar
            progress_width = board_width * (ply_count / total_plies)
            new_progress_bar = Rectangle(width=progress_width, height=0.3, fill_color=BLUE, fill_opacity=0.8, stroke_width=0)
            new_progress_bar.move_to(progress_bg.get_center())
            new_progress_bar.align_to(progress_bg, LEFT)
            new_progress_text = Text(f"Move {move_num}/{total_moves}", font_size=18).next_to(progress_bg, RIGHT, buff=0.3)
            
            self.play(
                Transform(progress_bar, new_progress_bar),
                Transform(progress_text, new_progress_text),
                run_time=0.2
            )
            
            self.wait(0.3)
        
        # Final position
        if MAX_MOVES < 0 or ply_count <= MAX_MOVES * 2:
            final_text = Text("Checkmate!", font_size=32, color=RED).shift(RIGHT * 3 + DOWN * 2.5)
            self.play(Write(final_text))
        
        self.wait(2)
