#############################################################
#    The idea is simple: I have a class that stores	    #
#	 source data and use functions to change the values.#
#    Since they are after all manipulating the values in    #
#    the data that is stored in the same class, we can      #
#    then visualize their interactions later.		    #
#############################################################

import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


class dataChanger(object):
	def __init__(self, data):
		self.data = data
		# get index for rejected cases
		self.rejected_index = self.data['SKP_CREDIT_STATUS'] == 8

		# set inclusion indexes because steps in Blaze are done in order. When the 
		# below functions are approving applications due to a low score, I need
		# to include only other possible text description cutoff categories
		self.na_exclude_index = ~self.data['TEXT_CUTOFF_DESC_PRE'].isin([
														'Low Sesame Score'
														'High Sesame score'])

		self.low_include_index = self.data['TEXT_CUTOFF_DESC_PRE'].isin(['Low Risk abc',
														'Low Risk Group bcd',
														'Low Risk Group def'])


	# change the data for one strategy's cutoff change
	def zhima_credit_status_changer(self, cutoff = None):
		low_index = self.data['ZHIMA_SCORE'] > 670
		temp_index = self.data[self.rejected_index & low_index & self.na_exclude_index &
							   (self.data['SCORE'] >= 0.18) &
							   (self.data['SCORE'] < cutoff)]
		self.data.loc[temp_index.index.tolist(), 'SKP_CREDIT_STATUS'] = 2
		return self.data

	# change the data for another strategy's cutoff change
	def low_9_credit_status_changer(self, cutoff = None):
		low_index = self.data['PRODUCT_RISK_GROUP'] == 'low'
		temp_index = self.data[self.rejected_index & low_index &
							self.low_include_index &
							   (self.data['SCORE'] >= 0.09) &
							   (self.data['SCORE'] < cutoff)]
		self.data.loc[temp_index.index.tolist(), 'SKP_CREDIT_STATUS'] = 2
		return self.data

	# FEEL FREE TO ADD IN MORE FUNCTIONS IN THIS CLASS FOR DATA MANIPULATION

# Take in the data after modifications by above functions
def AR_calculator(data):
    # get alternative type of 2, 3, 4 only
    data = data[(data['SKP_ALTERNATIVE_TYPE'].isin([2, 3, 4]))]
    total_number = data.shape[0]
    # Use Dataframe.isin() to get successful contracts
    list = [2, 3, 5, 6]
    number_of_success = data[data['SKP_CREDIT_STATUS'].isin(list).tolist()].shape[0]
    approval_rate = number_of_success / total_number
    return approval_rate


def main(cutoff1, cutoff2):
	data = pd.read_csv('abc.csv', encoding='ISO-8859-1')
	changer = dataChanger(data)
	changer.zhima_credit_status_changer(cutoff1)
	changer.low_9_credit_status_changer(cutoff2)
	AR = AR_calculator(changer.data)
	risk = 0.2   # set this to your function that calculates your risk
	print('Approval rate is ', round(AR*100,4), '%')
	return np.array([AR, risk])

# print(main(0.20))
fig = plt.figure()
ax = fig.add_subplot(211)
x = [1,2]
cutoff1 = 0.18
cutoff2 = 0.09
axis_color = 'lightgoldenrodyellow'
# Adjust the subplots region to leave some space for the sliders and buttons
fig.subplots_adjust(left=0.25, bottom=0.25)
ax.bar(x, main(cutoff1, cutoff2))
ax.set_ylim([0, 0.2])
ax.set_xticks(x)
ax.set_xticklabels([ 'AR', 'Just for fun'])

# Define an axes area and draw a slider in it
amp_slider_ax  = fig.add_axes([0.25, 0.48, 0.65, 0.03], axisbg=axis_color)
amp_slider = Slider(amp_slider_ax, 'Zhima cutoff', 0.18, 1, valinit=cutoff1)

# Define an axes area and draw a slider in it
amp_slider_ax1  = fig.add_axes([0.25, 0.44, 0.65, 0.03], axisbg=axis_color)
amp_slider1 = Slider(amp_slider_ax1, 'low 0.09 cutoff', 0.09, 0.22, valinit=cutoff2)

# Define an action for modifying the line when any slider's value changes
def sliders_on_changed(val):
	ax.clear()
	ax.bar(x, main(amp_slider.val, amp_slider1.val))
	ax.set_ylim([0, 0.2])
	ax.set_xticks(x)
	ax.set_xticklabels(['AR', 'Just for fun'])
amp_slider.on_changed(sliders_on_changed)
amp_slider1.on_changed(sliders_on_changed)

# Add a button for resetting the parameters
reset_button_ax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
def reset_button_on_clicked(mouse_event):
	amp_slider.reset()
	amp_slider1.reset()
	amp_slider2.reset()
reset_button.on_clicked(reset_button_on_clicked)

plt.show()

