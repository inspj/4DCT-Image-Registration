import argparse
import string
import json

def deformable_transform(name = '0', use_init=True, resolution = '6', f_grid_spacing = '10', iter_number = '1000', spatial_samples = '2000',
                         spacing_schedule = '16.0 8.0 8.0 4.0 2.0 1.0', pyramid_schedule = '16 16 16 8 8 8 4 4 4 2 2 2 1 1 1 1 1 1' , metric = 'AdvancedNormalizedCorrelation',bin=32, region=50.0, fill_value=0, ext='mhd'):

    name = f'B_Spline_{name}'

    template=string.Template('''
    
// Parameter File for B-Spline Registration

// Internal pixel type, "short" for saving memory
// "float" if that is not required
(FixedInternalImagePixelType "float")
(MovingInternalImagePixelType "float")

// Image dimension which is dependant if we 
// work with 2D or 3D etc.
(FixedImageDimension 3)
(MovingImageDimension 3)


(UseDirectionCosines "true")


// ----------- Main Component ---------

(Registration "MultiResolutionRegistration")
(Interpolator "BSplineInterpolator")

// Final Interpolator
(ResampleInterpolator "FinalBSplineInterpolator")
(Resampler "DefaultResampler")


// Image Pyramid strategy improves the capture range
// and robustness of a registration
(FixedImagePyramid "FixedRecursiveImagePyramid")
(MovingImagePyramid "MovingRecursiveImagePyramid")

// Important for quantitatively evaluating 
// difference between images 
(Optimizer "AdaptiveStochasticGradientDescent")
(Transform "BSplineTransform")
(Metric ${metric})  // OPTIMIZED BY QUANTITATIVE MEASURES
        
// ----------- Transformation -----------

// Reflects the desired type of transformation 
// and constrain the solution space to that type 
// of deformation

(FinalGridSpacingInPhysicalUnits ${f_grid_spacing}) // OPTIMIZED BY QUANTITATIVE MEASURES

(GridSpacingSchedule ${spacing_schedule}) // OPTIMIZED BY QUANTITATIVE MEASURES

(HowToCombineTransforms "Compose")
        
// ----------- Similarity measure -----------

(NumberOfHistogramBins ${bin}) // OPTIMIZED BY QUANTITATIVE MEASURES
        
// ----------- Multiresolution -----------

(NumberOfResolutions ${resolution}) // OPTIMIZED BY QUANTITATIVE MEASURES 
(ImagePyramidSchedule ${pyramid_schedule}) // OPTIMIZED BY QUANTITATIVE MEASURES

// ----------- Optimizer -----------

(MaximumNumberOfIterations ${iter_number}) // OPTIMIZED BY QUANTITATIVE MEASURES 
(AutomaticParameterEstimation "true") // OPTIMIZED BY QUANTITATIVE MEASURES 
(UseAdaptiveStepSizes "true")
(MaximumStepLength 1) // OPTIMIZED BY QUANTITATIVE MEASURES


// ----------- Image sampling -----------

(NumberOfSpatialSamples ${spatial_samples})  // OPTIMIZED BY QUANTITATIVE MEASURES
(NewSamplesEveryIteration "true")
(ImageSampler "RandomCoordinate")
(SampleRegionSize ${region})  // OPTIMIZED BY QUANTITATIVE MEASURES
(UseRandomSampleRegion "false")
(MaximumNumberOfSamplingAttempts 50)  // OPTIMIZED BY QUANTITATIVE MEASURES

// ----------- Interpolation and Resampling -----------

(BSplineInterpolationOrder 1)  // OPTIMIZED BY QUANTITATIVE MEASURES [0 1 2 3]
(FinalBSplineInterpolationOrder 3) // OPTIMIZED BY QUANTITATIVE MEASURES [0 1 2 3]
        
// ----------- Writing Stuffs -----------

(WriteTransformParametersEachIteration "false")
(WriteTransformParametersEachResolution "true")
(WriteResultImageAfterEachResolution "false")
(WritePyramidImagesAfterEachResolution "false")

(DefaultPixelValue ${fill_value})

(WriteResultImage "true")
(ResultImagePixelType "float")
(ResultImageFormat "${ext}")
    ''')

    param={
        'use_init': 'true' if use_init else 'false',
        'bin': bin,
        'resolution' : resolution,
        'f_grid_spacing': f_grid_spacing,
        'spacing_schedule': spacing_schedule,
        'pyramid_schedule': pyramid_schedule,
        'spatial_samples':  spatial_samples,
        'iter_number': iter_number,
        'metric':metric,
        'region': region,
        'fill_value': fill_value,
        'ext': ext
    }
    transform = template.substitute(param)

    return transform, name
