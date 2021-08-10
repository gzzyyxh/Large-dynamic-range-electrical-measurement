//AD7177-2 �����ɼ��ο����룬���������IOģ��SPI����ֲʱ����IO�������
//��AD7177-2�ļĴ��������߼�Ϊ��1��д��ͨ�żĴ�����ָʾ��һ�������Ķ�д������Ĵ�����ַ
//                              2��д����ȡ����
//AD7177-2��Ҫ����0x20�Ĵ�������24Bit��32Bitģʽ������
#include "stm32f10x_conf.h"

#define SCLK_H GPIO_SetBits(GPIOD,GPIO_Pin_3)
#define SCLK_L GPIO_ResetBits(GPIOD,GPIO_Pin_3)
#define SDI_H GPIO_SetBits(GPIOD,GPIO_Pin_2)
#define SDI_L GPIO_ResetBits(GPIOD,GPIO_Pin_2)
#define CS_H GPIO_SetBits(GPIOD,GPIO_Pin_1)
#define CS_L GPIO_ResetBits(GPIOD,GPIO_Pin_1)
#define SDO GPIO_ReadInputDataBit(GPIOD,GPIO_Pin_0)

void RCC_Configuration(void); 
void GPIO_Configuration(void);
void NVIC_Configuration(void); 
void Delay(vu32 nCount);
void AD7177_SPI_WB(uint8_t com);//SPI�ӿڣ��ֽڣ�д�뺯��
uint8_t AD7177_SPI_RB(void);//SPI�ӿڣ��ֽڣ���ȡ����
uint32_t AD7177_RDATA(void);//AD7177-2 ADC���ݶ�ȡ��������ȡ4Byte��
void AD7177_RESET(void);//AD7177-2 ��λ����
uint16_t Get_AD7177_ID(void);//��ȡAD7177-2 оƬID��ID��ֵΪ��0X4FDX;
void AD7177_INIT(void);//AD7177-2��ʼ������
uint16_t AD7177_Read_Reg(uint8_t addr);
float Get_Vol(void);

float Voltage;
uint16_t AD7177_ID;
uint32_t test;

int main(void) 
{ 
  RCC_Configuration();
  GPIO_Configuration();
  NVIC_Configuration();
  
  AD7177_RESET();//д������64��ʱ�Ӹ�λAD7177-2 SPI���ֽӿ�
  AD7177_ID=Get_AD7177_ID();//��ȡAD7177 ID 0X4FDX;
  AD7177_INIT();
  CS_L;
  while (1)   
  {
    /*
    while(SDO);
    test=AD7177_RDATA();//��ȡԭ��
    */
    Voltage=Get_Vol();//��ȡAIN0\AIN1�����ѹ
  } 
} 


uint32_t AD7177_RDATA(void)//
{
  uint32_t Rdata=0;
  for(uint8_t s=0;s<32;s++)
  {
    SCLK_L;
    Rdata<<=1;
    if(SDO)Rdata++;
    SCLK_H;
  }
  return Rdata;
}


float Get_Vol(void)
{
  float S_Vol;
  while(SDO);
  S_Vol=AD7177_RDATA();
  S_Vol = (S_Vol-0x80000000)/0x80000000*5*430/100;//��ѹ�ɼ������ϵ
  return S_Vol;
}


void AD7177_INIT(void)//Ӧ���źŲɼ���ʼ������
{
  CS_L;
  
  AD7177_SPI_WB(0x06);//GPIO ���üĴ���
  AD7177_SPI_WB(0x00);//
  AD7177_SPI_WB(0x0d);//д��0x0cʱ��D3��D5��
                      //д��0x0Fʱ��D3��D5��
                      //д��0x0eʱ��D3��D5��
                     //д��0x0dʱ��D3����D5��
  
  AD7177_SPI_WB(0x01);//дADCģʽ�Ĵ���
  AD7177_SPI_WB(0xa0);//ʹ���ڲ���׼���
  AD7177_SPI_WB(0x0c);//����ת��ģʽ���ⲿ����*/
  
  AD7177_SPI_WB(0x10);//дͨ��ӳ��Ĵ���0
  AD7177_SPI_WB(0x00);//ʹ��ͨ��0����ֹ��ͨ��
  AD7177_SPI_WB(0x01);//ADC+ -> AIN0;ADC- ->AIN1
  
  AD7177_SPI_WB(0x20);//д���üĴ���
  AD7177_SPI_WB(0x1f);//ʹ�ܻ�׼buf��AIN����buf��
  AD7177_SPI_WB(0x00);//
  
  AD7177_SPI_WB(0x28);//д�˲������üĴ���0
  AD7177_SPI_WB(0x00);//
  AD7177_SPI_WB(0x14);//0x07:10ksps   0x0A:1ksps  0x0f:59.92sps   0x14:5sps
  
  AD7177_SPI_WB(0x02);//д�ӿ�ģʽ�Ĵ���
  AD7177_SPI_WB(0x10);//
  AD7177_SPI_WB(0x82);//ʹ��32Bit�������
}


uint16_t Get_AD7177_ID(void)
{
  uint16_t ID;
  ID=0;
  CS_L;
  AD7177_SPI_WB(0x47);
  ID=AD7177_SPI_RB();
  ID<<=8;
  ID|=AD7177_SPI_RB();
  CS_H;
  return ID;
}


uint16_t AD7177_Read_Reg(uint8_t addr)
{
  uint16_t reg;
  CS_L;
  AD7177_SPI_WB(addr);
  reg=AD7177_SPI_RB();
  reg<<=8;
  reg|=AD7177_SPI_RB();
  CS_H;
  return reg;
}


void AD7177_RESET(void)
{
  SCLK_H;
  Delay(0xffff);
  CS_L;
  for(uint8_t a=0;a<10;a++)
  {
    AD7177_SPI_WB(0xff);
  }
  CS_H;
  Delay(0xffff);//�ȴ���λ��� 
  CS_L;
}


void AD7177_SPI_WB(uint8_t com)
{
  uint8_t com_temp=com;
  for(uint8_t s=0;s<8;s++)
  {
    if(com_temp&0x80)
    {
      SDI_H;
    }
    else
    {
      SDI_L;
    }
    SCLK_L;
    com_temp<<=1;
    SCLK_H;
  }
}


uint8_t AD7177_SPI_RB(void)
{
  uint8_t Rdata=0;
  for(uint8_t s=0;s<8;s++)
  {
    SCLK_L;
    Rdata<<=1;
    if(SDO)Rdata++;
    SCLK_H;
  }
  return Rdata;
}


void RCC_Configuration(void) 
{    
  ErrorStatus HSEStartUpStatus;
  RCC_DeInit(); 
  RCC_HSEConfig(RCC_HSE_ON); 
  HSEStartUpStatus = RCC_WaitForHSEStartUp(); 
  if(HSEStartUpStatus == SUCCESS) 
  { 
    FLASH_PrefetchBufferCmd(FLASH_PrefetchBuffer_Enable); 
    FLASH_SetLatency(FLASH_Latency_2); 
    RCC_HCLKConfig(RCC_SYSCLK_Div1);  
    RCC_PCLK2Config(RCC_HCLK_Div1);  
    RCC_PCLK1Config(RCC_HCLK_Div2); 
    RCC_PLLConfig(RCC_PLLSource_HSE_Div1, RCC_PLLMul_9); 
    RCC_PLLCmd(ENABLE); 
    while(RCC_GetFlagStatus(RCC_FLAG_PLLRDY) == RESET) { } 
    RCC_SYSCLKConfig(RCC_SYSCLKSource_PLLCLK); 
    while(RCC_GetSYSCLKSource() != 0x08) { } 
  } 
  RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA2, ENABLE); 
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO | RCC_APB2Periph_GPIOE| RCC_APB2Periph_GPIOD, ENABLE); 
} 

void GPIO_Configuration(void) 
{ 
  GPIO_InitTypeDef GPIO_InitStructure; 
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_1|GPIO_Pin_2|GPIO_Pin_3; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
  GPIO_Init(GPIOD, &GPIO_InitStructure); 
  
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
  GPIO_Init(GPIOE, &GPIO_InitStructure); 
  
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_0; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING; 
  GPIO_Init(GPIOD, &GPIO_InitStructure); 
} 


void NVIC_Configuration(void) 
{ 
#ifdef  VECT_TAB_RAM   
  NVIC_SetVectorTable(NVIC_VectTab_RAM, 0x0);  
#else
  NVIC_SetVectorTable(NVIC_VectTab_FLASH, 0x0);    
#endif 
} 

void Delay(vu32 nCount) 
{ 
  for(; nCount != 0; nCount--); 
} 

#ifdef  DEBUG 
void assert_failed(u8* file, u32 line) 
{  
  while (1) { } 
} 
#endif 