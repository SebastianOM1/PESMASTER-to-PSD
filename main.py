from request import get
from clip import to_clip
from countryinfo import CountryInfo

def to2013(dictionary):
  positions = ['GK', 'CB', 'SB', 'SB', 'DMF', 'CMF', 'SMF', 'SMF', 'AMF', 'WF', 'WF', 'SS', 'CF']
  injury = ['C', 'B', 'A']
  engagements = {
    'GK': [2,2],
    'CB': [1,3],
    'SB': [2,2],
    'DMF': [2,3],
    'CMF': [2,2],
    'SMF': [3,2],
    'AMF': [2,1],
    'WF': [3,2],
    'SS': [3,2],
    'CF': [3,1]
  }
  result = dict()
  
  result['Name'] = dictionary['name'].upper()
  
  result['Shirt Number'] = dictionary['squadnumber']
  try:
    result['Nationality'] = to_demonym(dictionary['nat_name']) if dictionary['nat_name'].lower() != 'england' else 'English'
  except:
    result['Nationality'] = 'Empty'
  result['Height'] = dictionary['height']
  result['Weight'] = dictionary['weight']
  result['Age'] = dictionary['age']
  result['Foot'] = 'L' if dictionary['foot'] else 'R'
  right_only = sum([1 if dictionary[pos] == 2 else 0 for pos in ['pos_rb', 'pos_rm', 'pos_rw']])
  left_only = sum([1 if dictionary[pos] == 2 else 0 for pos in ['pos_lb', 'pos_lm', 'pos_lw']])
  if right_only == left_only:
    result['Side'] = 'B'
  else:
    result['Side'] = 'R' if right_only > left_only else 'L'
  result['Main position'] = positions[dictionary['position']]
  position_list = [
    'pos_gk',
    'pos_cb',
    'pos_rb',
    'pos_lb',
    'pos_dm',
    'pos_cm',
    'pos_rm',
    'pos_lm',
    'pos_am',
    'pos_rw',
    'pos_lw',
    'pos_ss',
    'pos_cf'
  ]
  set_of_positions = set()
  for index in range(len(position_list)):
    if dictionary[position_list[index]] == 2:
      set_of_positions.add(positions[index])
  set_of_positions.remove(result['Main position'])
  result['Other positions'] = list(set_of_positions)
  
  result['Attack'] = min(99, dictionary['offensive_awareness'] + 10)
  result['Defence'] = dictionary['defensive_awareness'] if dictionary['position'] else min(99, dictionary['gk_awareness'] + 10)
  result['Header Accuracy'] = min(99, dictionary['heading'] + 10)
  result['Dribble Accuracy'] = min(99, (dictionary['dribbling'] + dictionary['tight_possession']) // 2 + 10)
  result['Short Pass Accuracy'] = min(99, dictionary['low_pass'] + 10)
  result['Short Pass Speed'] = min(99, (dictionary['low_pass'] + dictionary['kicking_power']) // 2 + 10)
  result['Long Pass Accuracy'] = min(99, dictionary['lofted_pass'] + 10)
  result['Long Pass Speed'] = min(99, (dictionary['lofted_pass'] + dictionary['kicking_power']) // 2 + 10)
  result['Shot Accuracy'] = min(99, dictionary['finishing'] + 10)
  result['Place Kicking'] = min(99, dictionary['set_piece_taking'] + 10)
  result['Swerve'] = min(99, dictionary['curl'] + 10)
  result['Ball Control'] = min(99, dictionary['ball_control'] + 10)
  # Possible wfa values: 0, 1, 2
  # 0 -> 3 or 4
  # 1 -> 5 or 6
  # 2 -> 7 or 8
  # Don't really want to make it random, will settle for lower instead.
  result['Weak Foot Accuracy'] = dictionary['weak_foot_acc'] * 2 + 3
  
  # Possible wff values: 0, 1, 2
  # 0 -> 3 or 4
  # 1 -> 5 or 6
  # 2 -> 7 or 8
  # Don't really want to make it random, will settle for lower instead.
  result['Weak Foot Frequency'] = dictionary['weak_foot_usage'] * 2 + 3
  
  result['Goal Keeping Skills'] = 50 if dictionary['position'] else min(99, (dictionary['gk_catching'] + dictionary['gk_parrying'] + dictionary['gk_reach']) // 3 + 10)
  
  att_response = (dictionary['offensive_awareness'] * 2 + dictionary['tackling']) // 3
  result['Response'] = (min(99, dictionary['tackling'] + 5) if dictionary['position'] < 6 else att_response) if dictionary['position'] else min(99, dictionary['gk_reflexes'] + 10)
  result['Explosive Power'] = min(99, (dictionary['balance'] + dictionary['acceleration']) // 2 + 10)
  result['Dribble Speed'] = min(99, (dictionary['tight_possession'] + dictionary['acceleration']) // 2 + 10)
  result['Top Speed'] = min(99, dictionary['speed'] + 10)
  
  result['Body Balance'] = min(99, dictionary['physical_contact'] + 10) if result['Main position'] in ['GK', 'CB', 'DMF'] else min(99, (dictionary['physical_contact'] + dictionary['balance']) // 2 + 10)
  result['Stamina'] = min(99, dictionary['stamina'] + 10)
  result['Kicking Power'] = min(99, dictionary['kicking_power'] + 10)
  result['Jump'] = min(99, dictionary['jumping'] + 10)
  # Possible values: 0, 1, 2
  # 0 -> C
  # 1 -> B
  # 2 -> A
  result['Injury Tolerance'] = injury[dictionary['injury_resistance']]
  
  result['Attack Awareness'] = engagements[result['Main position']][0]
  result['Defence Awareness'] = engagements[result['Main position']][1]
  # Possible form values: 0, 1, 2
  # 0 -> 3 or 4
  # 1 -> 5 or 6
  # 2 -> 7 or 8
  # Don't really want to make it random, will settle for lower instead.
  result['Form'] = dictionary['form'] * 2 + 3
  result['Tenacity'] = min(99, dictionary['aggression'] + 10)
  result['Teamwork'] = min(99, (dictionary['offensive_awareness'] + dictionary['defensive_engagement'] + dictionary['low_pass'] + dictionary['lofted_pass']) // 4 + 10)
  
  # Cards
  cards = []
  playing_style = dictionary['playing_style']
  if playing_style == 'Goal Poacher':
    cards.append('P12 - Goal Poacher')
  elif playing_style == 'Dummy Runner':
    cards.append('P13 - Dummy Runner')
  elif playing_style == 'Fox in the Box':
    cards.append('P16 - Fox In The Box')
    result['Attack Awareness'] = 3
    result['Defence Awareness'] = 1
  elif playing_style == 'Deep-Lying Forward':
    result['Defence Awareness'] = 2
  elif playing_style == 'Classic No. 10':
    cards.append('P01 - Classic N°10')
  elif playing_style == 'Hole Player':
    cards.append('P14 - Free Roaming')
    result['Attack Awareness'] = 3
  elif playing_style == 'Box-to-Box':
    cards.append('P08 - Box to Box')
    result['Attack Awareness'] = 3
    result['Defence Awareness'] = 3
  elif playing_style == 'The Destroyer':
    cards.append('P11 - Enforcer')
    result['Defence Awareness'] = 3
  elif playing_style == 'Anchor Man':
    cards.append('P02 - Anchor Man')
    result['Attack Awareness'] = 1
    result['Defence Awareness'] = 3
  elif playing_style in ['Offensive Full-back', 'Full-back Finisher', 'Extra Frontman']:
    cards.append('P17 - Offensive Fullback')
    result['Attack Awareness'] = 3
  elif playing_style == 'Defensive Full-back':
    result['Defence Awareness'] = 3
  
  if dictionary['trickster']:
    cards.append('P03 - Trickster')
  if dictionary['mazing_run']:
    cards.append('P05 - Mazing Run')
  if dictionary['speeding_bullet']:
    cards.append('P04 - Darting Run')
  if dictionary['incisive_run']:
    cards.append('P09 - Incisive Run')
  if dictionary['long_ball_expert']:
    cards.append('P06 - Pinpoint Pass')
  if dictionary['early_crosser']:
    cards.append('P07 - Early Cross')
  if dictionary['long_ranger']:
    cards.append('P10 - Long Ranger')
    
  if dictionary['s_first_time_shot'] or dictionary['s_one_touch_pass']:
    # S01
    cards.append('S01 - 1-touch Play')
    
  if dictionary['s_outside_curler']:
    # S02
    cards.append('S02 - Outside Curve')
    
  if dictionary['s_long_throw']:
    # S03
    cards.append('S03 - Long Throw')
    
  if dictionary['s_super_sub']:
    # S04
    cards.append('S04 - Super-Sub')
  
  if dictionary['s_long_range_curler'] or dictionary['s_long_range_shooting'] or dictionary['s_dipping_shot']:
    # S06
    cards.append('S06 - Long Range Drive')
    
  if dictionary['s_scotch_move']:
    # S07
    cards.append('S07 - Shoulder Feint Skills')
    
  if dictionary['s_chop_turn'] or dictionary['s_cut_behind_and_turn']:
    # S08
    cards.append('S08 - Turning Skills')
  
  if dictionary['s_marseille_turn']:
    # S09
    cards.append('S09 - Roulette Skills')
  
  if dictionary['s_flip_flap']:
    # S10
    cards.append('S10 - Flip Flap Skills')
  
  if dictionary['s_scissors_feint']:
    # S12
    cards.append('S12 - Scissors Skills')
    
  if dictionary['s_sole_control']:
    # S13
    cards.append('S13 - Step On Skills')
  
  if dictionary['s_knuckle_shot']:
    # S15
    cards.append('S15 - Knuckle Shot')
    
  if dictionary['s_acrobatic_finishing']:
    # S16 S17
    cards.append('S16 - Jumping Volley')
    cards.append('S17 - Scissor Kick')
    
  if dictionary['s_weighted_pass']:
    # S19
    cards.append('S19 - Weighted Pass')
    
  if dictionary['s_double_touch']:
    # S20
    cards.append('S20 - Double Touch')
    
  if dictionary['s_sombrero']:
    # S22
    cards.append('S22 - Sombrero')
    
  if dictionary['s_sliding_tackle']:
    # S24
    cards.append('S24 - Lunging Tackle')
    
  if dictionary['s_acrobatic_clearance']:
    # S25
    cards.append('S25 - Diving Header')
    
  if dictionary['s_gk_long_throw']:
    cards.append('S26 - GK Long Throw')
  
  if dictionary['s_track_back']:
    cards.append('P18 - Track Back')
    result['Defence Awareness'] = 3
  
  if dictionary['s_fighting_spirit']:
    result['Tenacity'] = min(99, result['Tenacity'] + 5)
    
  result['Cards'] = cards
    
  return result

def to_demonym(nation):
  country = CountryInfo(nation)
  return country.demonym()

def main():
  print('Enter a PESMASTER url: ', end='')
  url = input()
  dictionary_2022 = get(url)
  dictionary_2013 = to2013(dictionary_2022)
  to_clip(dictionary_2013)
  
if __name__ == '__main__':
  main()