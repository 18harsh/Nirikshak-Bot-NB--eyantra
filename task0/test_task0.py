try:
	import task0_cardinal

except ImportError:
	print("\n\t[ERROR] It seems that task0_cardinal.pyc is not found in current directory! OR")
	print("\n\tAlso, it might be that you are running test_task0.py from outside the Conda environment!\n")
	exit()


# Main function
if __name__ == '__main__':

	task0_cardinal.test_setup()