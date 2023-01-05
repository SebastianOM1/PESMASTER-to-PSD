import pyperclip

def to_clip(dictionary):
  cards = dictionary['Cards']
  result = 'Name: {0}\nShirt Name: {1}\nShirt Number: {2}\nNationality: {3}\nHeight: {4} cm\nWeight: {5} kg\n'.format(
    dictionary['Name'],
    dictionary['Name'],
    dictionary['Shirt Number'],
    dictionary['Nationality'],
    dictionary['Height'],
    dictionary['Weight']
  )
  result += 'Age: {0} (01/01/1980)\nFoot: {1}\nSide: {2}\nPositions: {3}★, {4}'.format(
    dictionary['Age'],
    dictionary['Foot'],
    dictionary['Side'],
    dictionary['Main position'],
    str(dictionary['Other positions'])[1:-1].replace("'", '')
  )
  
  result += '\n\n\nTECHNIQUE\n'
  result += 'Attack: {0}\nDefence: {1}\nHeader Accuracy: {2}\nDribble Accuracy: {3}\nShort Pass Accuracy: {4}\n'.format(
    dictionary['Attack'],
    dictionary['Defence'],
    dictionary['Header Accuracy'],
    dictionary['Dribble Accuracy'],
    dictionary['Short Pass Accuracy']
  )
  result += 'Short Pass Speed: {0}\nLong Pass Accuracy: {1}\nLong Pass Speed: {2}\nShot Accuracy: {3}\nPlace Kicking: {4}\n'.format(
    dictionary['Short Pass Speed'],
    dictionary['Long Pass Accuracy'],
    dictionary['Long Pass Speed'],
    dictionary['Shot Accuracy'],
    dictionary['Place Kicking']
  )
  result += 'Swerve: {0}\nBall Controll: {1}\nGoal Keeping Skills: {2}\nWeak Foot Accuracy: {3}\nWeak Foot Frequency: {4}'.format(
    dictionary['Swerve'],
    dictionary['Ball Control'],
    dictionary['Goal Keeping Skills'],
    dictionary['Weak Foot Accuracy'],
    dictionary['Weak Foot Frequency']
  )
  
  result += '\nSPEED\n'
  result += 'Response: {0}\nExplosive Power: {1}\nDribble Speed: {2}\nTop Speed: {3}'.format(
    dictionary['Response'],
    dictionary['Explosive Power'],
    dictionary['Dribble Speed'],
    dictionary['Top Speed']
  )

  result += '\nPHYSICAL\n'
  result += 'Body Balance: {0}\nStamina: {1}\nKicking Power: {2}\nJump: {3}\nInjury Tolerance: {4}'.format(
    dictionary['Body Balance'],
    dictionary['Stamina'],
    dictionary['Kicking Power'],
    dictionary['Jump'],
    dictionary['Injury Tolerance']
  )
  
  result += '\nRESISTANCE\n'
  result += 'Attack Awareness: {0}\nDefence Awareness: {1}\nForm: {2}\nTenacity: {3}\nTeamwork: {4}'.format(
    dictionary['Attack Awareness'],
    dictionary['Defence Awareness'],
    dictionary['Form'],
    dictionary['Tenacity'],
    dictionary['Teamwork']
  )
  
  result += '\n\n\n\n\nPLAYER INDEX CARDS:\n'
  # [P or S][00] - [Name]
  added_cards = 0
  for card in sorted(cards):
    if added_cards < 11:
      result += card
      result += '\n'
      added_cards += 1
  
  pyperclip.copy(result)