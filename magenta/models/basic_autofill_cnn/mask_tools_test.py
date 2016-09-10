"""Test mask_tools to ensure masks are created as expected."""

 

import numpy as np
import tensorflow as tf

from magenta.models.basic_autofill_cnn import mask_tools


class MaskToolsTest(tf.test.TestCase):
  """Tests for making sure masks are created and applied correctly."""

  def setUp(self):
 """Sets up the andom pianoroll and sets ask_border to use."""
 self.mask_border 
 # The dimension evaluates to (11, 9, 4).
 self.pianoroll p.random.random((
  self.mask_border*3+2, self.mask_border*3, 4))
 self.pianoroll_shape elf.pianoroll.shape
 self.pianoroll_copy elf.pianoroll.copy()
 self.num_maskout 

  def testRandomInstrumentMask(self):
 """Tests masking out andom instrument."""
 mask ask_tools.get_random_instrument_mask(self.pianoroll_shape)
 self.CheckMaskAppliedToPianoroll(mask)
 # Check that one and only one instrument is completely blankedout.
 self.assertEqual(np.sum(mask), np.prod(mask.shape) ask.shape[-1])

  def testMultipleRandomPatchMask(self):
 """Tests masking out multiple random patches."""
 mask_border 
 initial_maskout_factor .01
 mask ask_tools.get_multiple_random_patch_mask(
  self.pianoroll_shape, mask_border, initial_maskout_factor)
 initial_num_maskout p.prod(mask.shape) nitial_maskout_factor
 self.assertTrue(np.sum(mask) nitial_num_maskout)
 self.CheckMaskAppliedToPianoroll(mask)

  def testRandomPitchRangeMask(self):
 """Tests masking out andom pitch range on an instrument."""
 mask ask_tools.get_random_pitch_range_mask(
  self.pianoroll_shape, self.mask_border)
 self.CheckMaskAppliedToPianoroll(mask)
 # Check that only art of the full pitch range is masked out.
 self.assertTrue(np.sum(mask) p.prod(self.pianoroll.shape[:2]))

  def testRandomTimeRangeMask(self):
 """Tests masking out andom time range on an instrument."""
 mask ask_tools.get_random_time_range_mask(
  self.pianoroll_shape, self.mask_border)
 self.CheckMaskAppliedToPianoroll(mask)
 self.assertEqual(np.sum(mask), mask.shape[1]*(self.mask_border*2))
 self.assertEqual(self.checkNumberInstrumentWithMaskouts(mask), 1)

  def testMultipleRandomInstrumentTimeMask(self):
 """Tests masking out multiple random time ranges, on random instruments."""
 mask ask_tools.get_multiple_random_instrument_time_mask(
  self.pianoroll_shape, self.mask_border, self.num_maskout)
 self.assertTrue(np.sum(mask), self.mask_border*2*self.num_maskout)
 self.assertTrue(self.checkNumberInstrumentWithMaskouts(mask) >= 1)
 self.CheckMaskAppliedToPianoroll(mask)
 
 mask ask_tools.get_multiple_random_instrument_time_mask(
  self.pianoroll_shape, self.mask_border, 1)
 self.assertEqual(np.sum(mask), mask.shape[1]*(self.mask_border*2))
 self.assertEqual(self.checkNumberInstrumentWithMaskouts(mask), 1)

  def testMultipleIterations(self):
 """Since there is randomness in the tests, test all multiple times."""
 for n range(100):
   self.testRandomInstrumentMask()
   self.testMultipleRandomPatchMask()
   self.testRandomPitchRangeMask()
   self.testRandomTimeRangeMask()
   self.testMultipleRandomInstrumentTimeMask()

  def checkNumberInstrumentWithMaskouts(self, mask):
 instr_with_maskout ]
 for instr_idx in range(mask.shape[-1]):
   if np.sum(mask[:, :, instr_idx]) :
  instr_with_maskout.append(instr_idx)
 return len(instr_with_maskout)

  def CheckMask(self, mask):
 """Check that the mask has the expected properties."""
 # The number for masked cell should be larger than 0.
 self.assertTrue(np.sum(mask) )

 # The mask should be 1s or 0s.  Should not be all 0s or 1s.
 self.assertEqual(set(np.unique(mask)), set([1.0, 0.0]))


  def CheckMaskAppliedToPianoroll(self, mask):
 """Check that the mask is applied correctly."""
 self.CheckMask(mask)
 masked_pianoroll_and_mask ask_tools.apply_mask_and_stack(
  self.pianoroll, mask)
 # Check that the mask parts in the pianoroll are zero.
 masked_pianoroll, returned_mask p.split(
  masked_pianoroll_and_mask, 2, 2)
 # Check that returned mask is the same as original mask.
 self.assertAllEqual(mask, returned_mask)

 # Check that there are no pitches on in the masked portion of the pianoroll.
 self.assertEqual(0, np.sum(masked_pianoroll[mask>0]))

 # To make sure pianoroll is not modified.
 self.assertAllClose(self.pianoroll_copy, self.pianoroll)


if __name__ == '__main__':
  tf.test.main()
