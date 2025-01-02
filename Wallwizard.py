def within_bounds(x, y):
        return 0 <= x < 9 and 0 <= y < 9


def adjacent_move( x, y,new_x, new_y ):
        return abs(new_x - x) + abs(new_y - y) == 1


def blocked_by_wall( x, y, new_x, new_y ):
    
    for wx, wy, orientation in walls:
        if orientation == "H" and wy == max(y, new_y) and wx <= x < wx + 2:
            return True
        if orientation == "V" and wx == max(x, new_x) and wy <= y < wy + 2:
            return True
    return False


def is_valid_move(player, new_pos):
    
    x, y = player_positions[player]
    new_x, new_y = new_pos

    if not within_bounds(new_x, new_y ):
        return False

    if not adjacent_move( x, y, new_x, new_y ):
        return False

    if blocked_by_wall(x, y, new_x, new_y ):
        return False

    return True

def jamp (player, new_pos):
    x, y = player_positions[player]
    new_x, new_y = new_pos

    if not is_valid_move(player, new_pos):
        return False
        
    opp = 1 - player 
    opp_x, opp_y = player_positions[opp]

    if new_pos == (opp_x, opp_y): 
        dx = opp_x - x
        dy = opp_y - y
        jump_x = opp_x + dx
        jump_y = opp_y + dy

       
        if not within_bounds(jump_x, jump_y ):
            return False
        if blocked_by_wall(x, y, jump_x, jump_y ):
          return False
        else:
             player_positions[player] = (jump_x, jump_y) 
             return True

        
   
    
